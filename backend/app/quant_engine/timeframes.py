import pandas as pd


TIMEFRAME_TO_DAYS = {
    "1M": 21,
    "3M": 63,
    "6M": 126,
    "1Y": 252,
    "3Y": 756,
    "5Y": 1260,
}


def apply_timeframe(df: pd.DataFrame, timeframe: str = "1Y") -> pd.DataFrame:
    """
    Slice a dataframe to the selected trading-day window.
    """
    days = TIMEFRAME_TO_DAYS.get(timeframe.upper(), 252)

    if len(df) <= days:
        return df

    return df.tail(days)