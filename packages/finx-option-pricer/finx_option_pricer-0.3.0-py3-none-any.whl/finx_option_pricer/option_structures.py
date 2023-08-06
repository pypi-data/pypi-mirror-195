from typing import List

from finx_option_pricer.option import CALL, D_ONE, PUT, DeltaHedge, Option
from finx_option_pricer.option_plot import OptionPosition

MARKET_DAYS_PER_YEAR_US_STOCK = 252
RATE_ZERO = 0.0


def annualized_days(days: float, market_days_per_year=MARKET_DAYS_PER_YEAR_US_STOCK) -> float:
    """
    Convert days to decimal years

    Args:
        days(float): number of days

    Returns:
        float: fractional years (eg, 30 days / 252 => 0.119)
    """
    return days / market_days_per_year


def gen_combo(
    spot_price: float,
    input_list: List[dict],
) -> List[OptionPosition]:
    """
    Generate a combo structure of 1 or more options

    Assumes interest rate is 0.0
    """
    # for row in input_list:
    #     for expected_key in ["strike", "dte", "ivfront", "option_type", "trade_price"]:
    #         assert expected_key in row, f"Missing expected input key={expected_key} in {row.keys()}"

    combo = []

    for input_row in input_list:
        option_type = input_row["option_type"]
        assert option_type in [CALL, PUT, D_ONE], f"Invalid option_type={option_type}"

        trade_price = (
            float(input_row["trade_price"])
            if (input_row["trade_price"] is not None and input_row["trade_price"] != "")
            else None
        )

        if option_type in [CALL, PUT]:
            instrument = Option(
                S=spot_price,
                K=float(input_row["strike"]),
                T=annualized_days(float(input_row["dte"])),
                r=float(RATE_ZERO),
                sigma=float(input_row["ivfront"]),
                option_type=option_type,
            )
        elif option_type == D_ONE:
            instrument = DeltaHedge(S=spot_price, entry_price=trade_price)

        quantity = float(input_row["quantity"])
        option_position = OptionPosition(instrument=instrument, quantity=quantity, trade_price=trade_price)
        combo.append(option_position)

    return combo


def gen_calendar(
    spot_price: float,
    strike_price: float,
    front_days: int,
    front_vol: float,
    front_vol_final: float,
    back_days: int,
    back_vol: float,
    back_vol_final: float,
    option_type: str = "c",
) -> List[OptionPosition]:
    """
    Generate a calendar structure

    Assumes
    - interest rate is 0.0

    Returns: List[OptionPosition]
    """
    fs = front_vol
    fsf = front_vol_final
    bs = back_vol
    bsf = back_vol_final

    front = OptionPosition(
        quantity=-1,
        end_sigma=fsf,
        option=Option(
            S=spot_price, K=strike_price, T=annualized_days(front_days), r=RATE_ZERO, sigma=fs, option_type=option_type
        ),
    )

    back = OptionPosition(
        quantity=+1,
        end_sigma=bsf,
        option=Option(
            S=spot_price, K=strike_price, T=annualized_days(back_days), r=RATE_ZERO, sigma=bs, option_type=option_type
        ),
    )

    return [front, back]


def gen_strangle(
    spot_price: float,
    strike_price: float,
    days: int,
    vol_initial: float,
    vol_final: float,
) -> List[OptionPosition]:
    """
    Generate strangle

    Assumes
    - interest rate is 0.0

    Returns: List[OptionPosition]
    """

    short_call = OptionPosition(
        quantity=-1,
        end_sigma=vol_final,
        option=Option(
            S=spot_price,
            K=strike_price,
            T=annualized_days(days),
            r=RATE_ZERO,
            sigma=vol_initial,
            option_type="c",
        ),
    )

    short_put = OptionPosition(
        quantity=-1,
        end_sigma=vol_final,
        option=Option(
            S=spot_price,
            K=strike_price,
            T=annualized_days(days),
            r=RATE_ZERO,
            sigma=vol_initial,
            option_type="p",
        ),
    )

    return [short_call, short_put]
