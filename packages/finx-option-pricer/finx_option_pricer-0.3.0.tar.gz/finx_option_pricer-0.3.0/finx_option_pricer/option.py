from abc import ABCMeta
from dataclasses import dataclass
from typing import Literal

import finx_option_pricer.bsm as bsm

CALL = "c"
PUT = "p"
D_ONE = "d1"

MARKET_DAYS_PER_YEAR = 252

# DOLLAR_VALUE = "value"
# DELTA = "delta"
# GAMMA = "gamma"
# VEGA = "vega"
# THETA = "theta"
# RHO = "rho"

ALGO_BSM = "bsm"

# ALGO_SPACE_OPTION_TYPE_TO_FUNC_MAP = {
#     ALGO_BSM: {
#         DOLLAR_VALUE: {
#             CALL: bsm.bs_call_value,
#             PUT: bsm.bs_put_value,
#         },
#         DELTA: {
#             CALL: bsm.delta_call,
#             PUT: bsm.delta_put,
#         },
#     },
# }


# def calc_delta(S: float, K: float, T: float, r: float, sigma: float, option_type: str, algo: str=ALGO_BSM):
#     try:
#         func = ALGO_SPACE_OPTION_TYPE_TO_FUNC_MAP[algo][DELTA][option_type]
#     except KeyError:
#         raise ValueError(f"Invalid algo={algo} or option_type={option_type}")
#     return func(S, K, T, r, sigma)


# def calc_value(S: float, K: float, T: float, r: float, sigma: float, option_type: str, algo: str = ALGO_BSM):
#     try:
#         func = ALGO_SPACE_OPTION_TYPE_TO_FUNC_MAP[algo][DOLLAR_VALUE][option_type]
#     except KeyError:
#         raise ValueError(f"Invalid algo={algo} or option_type={option_type}")
#     return func(S, K, T, r, sigma)


class Instrument(metaclass=ABCMeta):
    @property
    def id(self) -> str:
        raise NotImplementedError

    @property
    def value(self) -> float:
        raise NotImplementedError

    @property
    def final_value(self) -> float:
        raise NotImplementedError

    @property
    def break_even_value(self) -> float:
        raise NotImplementedError

    @property
    def extrinsic(self) -> float:
        raise NotImplementedError

    @property
    def intrinsic(self) -> float:
        raise NotImplementedError

    @property
    def delta(self) -> float:
        raise NotImplementedError

    @property
    def gamma(self) -> float:
        raise NotImplementedError

    @property
    def vega(self) -> float:
        raise NotImplementedError

    @property
    def theta(self) -> float:
        raise NotImplementedError

    @property
    def rho(self) -> float:
        raise NotImplementedError


@dataclass
class DeltaHedge(Instrument):
    S: float  # spot price
    entry_price: float  # entry price

    @property
    def id(self) -> str:
        """
        Generate unique identifier for delta one hedge
        """
        id_values = [
            self.entry_price,
            D_ONE,
        ]
        return "-".join([str(x) for x in id_values])

    @property
    def value(self) -> float:
        """
        Calculate value of hedge in dollar space
        """
        return self.S

    @property
    def final_value(self) -> float:
        """
        Calculate final value of hedge in dollar space.
        NOTE - this is the same as value and calls that function.
        """
        return 0.0

    @property
    def iv(self) -> float:
        """
        Calculate implied volatility of hedge
        """
        return 0.0

    @property
    def break_even_value(self) -> float:
        """
        Calculate break even value of hedge
        """
        raise NotImplementedError

    @property
    def extrinsic(self) -> float:
        """
        Calculate extrinsic value of hedge
        """
        raise NotImplementedError

    @property
    def intrinsic(self) -> float:
        """
        Calculate intrinsic value of hedge
        """
        raise NotImplementedError

    @property
    def time_value(self) -> float:
        """
        Calculate time value of hedge
        """
        raise NotImplementedError

    @property
    def delta(self) -> float:
        """
        Calculate delta of hedge
        """
        return 1.0

    @property
    def gamma(self) -> float:
        """
        Calculate gamma of hedge
        """
        return 0.0

    @property
    def vega(self) -> float:
        """
        Calculate vega of hedge
        """
        return 0.0

    @property
    def theta(self) -> float:
        """
        Calculate theta of hedge
        """
        raise NotImplementedError

    @property
    def rho(self) -> float:
        """
        Calculate rho of hedge
        """
        raise NotImplementedError

    @property
    def T(self) -> float:
        """
        Calculate time to maturity of hedge
        """
        return 100.0

    @property
    def K(self) -> float:
        return 0.0


@dataclass
class Option(Instrument):
    S: float  # current price
    K: float  # strike price
    T: float  # time to maturity (in years, 0.5 => 6 months)
    r: float  # risk free rate
    # q: float # dividend rate
    sigma: float  # volatility
    option_type: Literal["c", "p"]
    algo: str = "bsm"
    market_days_per_year: int = MARKET_DAYS_PER_YEAR

    @property
    def _t_days(self) -> int:
        """Time in days"""
        return int(self.T * self.market_days_per_year)

    @property
    def id(self) -> str:
        """Generate unique identifier for option contract as priced by respective algo"""
        id_values = [
            self.K,
            self._t_days,
            self.r,
            self.sigma,
            self.option_type,
            self.algo,
        ]
        return "-".join([str(x) for x in id_values])

    @property
    def value(self) -> float:
        """Option value wrt to algo"""
        func = None
        if self.option_type == "c":
            func = bsm.bs_call_value
        elif self.option_type == "p":
            func = bsm.bs_put_value
        return func(self.S, self.K, self.T, self.r, self.sigma)

    @property
    def final_value(self) -> float:
        """Final value of option at expiration"""
        return self.instrument_value

    @property
    def break_even_value(self) -> float:
        """Break even value for option

        Call, be_value = Strike + Call Value
        Put, be_value = Strike - Put Value
        """
        # add or subtract depending if Call or Put
        _value = self.value * (1 if self.option_type == "c" else -1) * 1.0
        return self.K + _value

    @property
    def extrinsic_value(self) -> float:
        """Extrinsic value = option price - intrinsic value"""
        return self.value - self.intrinsic_value

    @property
    def intrinsic_value(self) -> float:
        """Intrinsic value = current (underlying) price - option price

        Returns:
            float: intrinsic value
        """
        return max(self.S - self.K, 0)

    @property
    def time_value(self) -> float:
        """Calc time value, defined as,
        Time Value = option value - intrinsic value
        https://www.investopedia.com/terms/t/timevalue.asp

        Returns:
            float: time_value
        """
        return self.value - self.intrinsic_value

    @property
    def delta(self) -> float:
        func = None
        if self.option_type == "c":
            func = bsm.delta_call
        elif self.option_type == "p":
            func = bsm.delta_put
        return func(self.S, self.K, self.T, self.r, self.sigma)

    @property
    def gamma(self) -> float:
        return bsm.gamma(self.S, self.K, self.T, self.r, self.sigma)

    @property
    def vega(self) -> float:
        return bsm.vega(self.S, self.K, self.T, self.r, self.sigma)

    @property
    def theta(self) -> float:
        func = None
        if self.option_type == "c":
            func = bsm.theta_call
        elif self.option_type == "p":
            func = bsm.theta_put
        return func(self.S, self.K, self.T, self.r, self.sigma)

    @property
    def rho(self) -> float:
        func = None
        if self.option_type == "c":
            func = bsm.rho_call
        elif self.option_type == "p":
            func = bsm.rho_put
        return func(self.S, self.K, self.T, self.r, self.sigma)

    def iv(self, opt_value: float) -> float:
        """Calculated Implied Volatility based on opt_price"""
        if self.option_type == CALL:
            return bsm.implied_vol_call(opt_value, self.S, self.K, self.T, self.r)
        if self.option_type == PUT:
            return bsm.implied_vol_put(opt_value, self.S, self.K, self.T, self.r)
        raise ValueError(f"Must select either c or p (for call or put). Presently, self.option_type={self.option_type}")
