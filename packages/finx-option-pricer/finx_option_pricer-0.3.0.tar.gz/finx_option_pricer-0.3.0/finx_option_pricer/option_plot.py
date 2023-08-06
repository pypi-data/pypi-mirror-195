from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd

from finx_option_pricer.option import DeltaHedge, Instrument, Option

MARKET_DAYS_PER_YEAR_US_STOCK = 252


def gen_range_floats(start, stop_at, step):
    """
    Generate a range of floats
    Returns: np.ndarray
    """
    stop_before = stop_at + step
    return np.arange(start, stop_before, step)


@dataclass
class OptionPosition:
    instrument: Instrument
    quantity: float
    end_sigma: float = None
    trade_price: float = None

    SHORT = "short"
    LONG = "long"

    @property
    def id(self):
        side = self.LONG if self.quantity >= 1 else self.SHORT
        qty = abs(self.quantity)
        return f"{self.option.id}-{side}{qty}"

    @property
    def value(self) -> float:
        return self.instrument.value * self.quantity

    @property
    def trade_value(self) -> float:
        return self.trade_price * self.quantity

    def interpolated_vol(self, fraction: float) -> float:
        """Using the start and end IV, calc the linearly interpolated IV"""
        assert self.end_sigma is not None, "end_sigma must be not None"
        return self.instrument.sigma - (self.instrument.sigma - self.end_sigma) * fraction

    def calc_pnl(self) -> float:
        """Calculate the PnL with respect to the traded_price"""
        assert self.trade_price is not None, "trade_price must be not None"
        return (self.instrument.value - self.trade_price) * self.quantity

    @property
    def cost_basis(self) -> float:
        """Calculate the cost basis"""
        if self.trade_price is not None:
            return self.trade_value
        else:
            return self.value


@dataclass
class OptionsPlot:
    """
    Options Plot takes a list of Option Positions with params for
    - spot_range
    - strike_interval

    And calculates how the composite position changes with respect strike/time in,
    - PnL space (value)
    - Time Value space (time_value)
    - Delta space (delta)
    - Vega space (vega)
    - Theta space (theta)
    - Gamma space (gamma)
    - Vanna space (TODO)
    - Volga space (TODO)
    - Charm space (TODO)
    """

    option_positions: List[OptionPosition]
    spot_range: List
    strike_interval: float = 0.5

    @property
    def value(self) -> float:
        """
        Returns a sum of the option_positions expected fair value

        Returns:
            float: aggregate value for self.option_options
        """
        total_value = 0.0
        for op in self.option_positions:
            total_value += op.value
        return total_value

    def _calc_op_attr_at_T(self, option_position, 
        option_attr: str, 
        newT: float, 
        spot_prices: np.ndarray,
        sigma_override=None
    ):
        """
        Calc `attr` for OptionPosition with respect to newT across range of spot prices.

        `attr` is an Option property, e.g. value, delta, vega, theta, gamma

        Args:
            option_position (OptionPosition): option position to calc attr for
            option_attr (str): property to calc: [value, delta, vega, theta, gamma, etc]
            newT (float): time to expiry for option
            spot_prices (np.ndarray): range of spot prices to calc attr for

        Returns:
            pd.Series: index = strikes, values = option_attr
        """
        values = []
        indexes = []

        for sp in spot_prices:
            if isinstance(option_position.instrument, Option):
                sigma = sigma_override if sigma_override is not None else option_position.instrument.sigma
                updated_i = Option(
                    S=sp,
                    K=option_position.instrument.K,
                    T=newT,
                    r=option_position.instrument.r,
                    sigma=sigma,
                    option_type=option_position.instrument.option_type,
                )
            elif isinstance(option_position.instrument, DeltaHedge):
                updated_i = DeltaHedge(
                    S=sp,
                    entry_price=sp,
                )

            val = getattr(updated_i, option_attr)
            values.append(val * option_position.quantity)
            indexes.append(sp)

        return pd.Series(values, index=indexes)

    def calc_option_attr_across_T(
        self, 
        option_attr: str, 
        days: int, 
        day_step: int=1,
        show_final=False, 
        value_relative=False,
        time_specific_iv={}
    ):
        """
        For option position, calc option attr across time for given strikes.

        Args:
            option_attr (str): property to calc: [value, delta, vega, theta, gamma,]
            days (int): number of days into the future to calc delta
            day_step (int, optional): step size for days. Defaults to 1.
            show_final (bool, optional): show final day. Defaults to False.
            value_relative (bool, optional): show relative change from t0. Defaults to False.
            time_specific_iv (dict, optional): time specific IV. Defaults to {}.

        Example return,

        strikes     t+0       t+1       t+2
        85.0        -1.358147 -1.858064 -1.9741
        85.5        -1.255539 -1.823718 -1.9741
        86.0        -1.139727 -1.781053 -1.9741
        86.5        -1.009635 -1.728572 -1.9741

        Args:
            option_attr (str): property to calc: [value, delta, vega, theta, gamma,]
            days (int): number of days into the future to calc delta
            day_step (int, optional): step size for days. Defaults to 1.
            show_final (bool, optional): show final day. Defaults to False.
            value_relative (bool, optional): show relative change from t0. Defaults to False.

        Returns:
            pd.DataFrame: index = strikes, columns = time into future (t+0, t+1, t+2, ... t+n)
        """
        min_dte = min([op.instrument.T for op in self.option_positions if op.instrument.T > 0])
        min_days = int(min_dte * MARKET_DAYS_PER_YEAR_US_STOCK)
        days_into_future = [x for x in range(0, days + 1, day_step) if x <= min_days]

        if show_final and min_days not in days_into_future:
            days_into_future.append(min_days)

        spot_prices = gen_range_floats(self.spot_range[0], self.spot_range[1], self.strike_interval)
        df = pd.DataFrame({"spot_prices": spot_prices}).set_index("spot_prices")

        # increment by day(int) into the future
        for day_into_future in days_into_future:
            op_positions_series = []
            for op in self.option_positions:
                T_to_expiration = op.instrument.T - (day_into_future / MARKET_DAYS_PER_YEAR_US_STOCK)

                overrides = {}
                if day_into_future in time_specific_iv:
                    overrides["sigma_override"] = time_specific_iv[day_into_future]

                series = self._calc_op_attr_at_T(op, option_attr, T_to_expiration, spot_prices, **overrides)

                op_positions_series.append(series)

            # sum too get agg of attribute value for each strike and assign to df (indexed by strike)
            df[f"t+{day_into_future}"] = pd.Series(sum(op_positions_series))

        # calc change relative to first day values
        if value_relative:
            spot_prices = list(set([x.instrument.S for x in self.option_positions]))
            assert len(spot_prices) == 1, "All positions should be configured with the same spot price"
            spot_price = spot_prices[0]
            initial_time_column = df.columns[0]
            t0 = df.loc[spot_price, initial_time_column].copy()
            return df.sub(t0)
        else:
            return df

    def gen_value_df_timeincrementing(
        self,
        days: int,
        step: int = 1,
        show_final: bool = True,
        market_days_year: int = 252,
        value_relative: bool = True,
    ) -> pd.DataFrame:
        """
        Generate value option positions as they decay with time.

        Example return,

        strikes     10         5       0
        85.0        -1.358147 -1.858064 -1.9741
        85.5        -1.255539 -1.823718 -1.9741
        86.0        -1.139727 -1.781053 -1.9741
        86.5        -1.009635 -1.728572 -1.9741

        Args:
            days (int): number days to increment over.
            step (int, optional): step or increment interval. Defaults to 1.
            show_final (bool, optional): option(s) value at expiration of nearest data option. Defaults to True.
            market_days_year(int): number of market days in a calendar year. Defaults to 252.
            value_relative(boolean): value the options package with respect to
                initial value vs absolute value. Defaults to True.

        Returns:
            (pd.DataFrame): DataFrame with columns [strikes, days-step1, days-step2, ..., expiration]
        """
        return self.calc_option_attr_across_T(
            "value",
            days,
            day_step=step,
            show_final=show_final,
            value_relative=value_relative,
        )
