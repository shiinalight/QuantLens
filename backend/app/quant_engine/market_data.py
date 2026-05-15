import numpy as np
import pandas as pd
import yfinance as yf


def fetch_price_history(ticker: str = "SPY", period: str = "1y"):
    data = yf.download(
        ticker,
        period=period,
        auto_adjust=True,
        progress=False,
        group_by="column",
    )

    if data.empty:
        raise ValueError(f"No data found for ticker: {ticker}")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()

    prices = []
    for _, row in data.iterrows():
        date_value = pd.to_datetime(row["Date"])

        prices.append(
            {
                "date": date_value.strftime("%Y-%m-%d"),
                "close": round(float(row["Close"]), 2),
                "volume": int(row["Volume"]),
            }
        )

    return prices


def build_market_payload(ticker: str = "SPY"):
    prices = fetch_price_history(ticker)

    df = pd.DataFrame(prices)
    df["date_dt"] = pd.to_datetime(df["date"])
    df["returns"] = df["close"].pct_change()
    df["equity"] = (1 + df["returns"].fillna(0)).cumprod() * 100
    df["rolling_max"] = df["equity"].cummax()
    df["drawdown"] = (df["equity"] / df["rolling_max"] - 1) * 100

    monthly_df = df.copy()
    monthly_df["month"] = monthly_df["date_dt"].dt.strftime("%b %y")
    monthly_returns = (
        monthly_df.groupby("month")["close"]
        .agg(lambda x: (x.iloc[-1] / x.iloc[0] - 1) * 100)
        .reset_index()
    )

    monthly = [
        {"month": row["month"], "return": round(float(row["close"]), 2)}
        for _, row in monthly_returns.iterrows()
    ]

    total_return = ((df["close"].iloc[-1] / df["close"].iloc[0]) - 1) * 100
    volatility = df["returns"].std() * np.sqrt(252) * 100

    average_daily_return = df["returns"].mean()
    daily_volatility = df["returns"].std()
    sharpe_ratio = (
        (average_daily_return / daily_volatility) * np.sqrt(252)
        if daily_volatility != 0
        else 0
    )

    max_drawdown = df["drawdown"].min()

    equity = [
        {"date": row["date"], "value": round(float(row["equity"]), 2)}
        for _, row in df.iterrows()
    ]

    drawdown = [
        {"date": row["date"], "dd": round(float(row["drawdown"]), 2)}
        for _, row in df.iterrows()
    ]

    return {
        "ticker": ticker,
        "price": round(float(df["close"].iloc[-1]), 2),
        "total_return": round(float(total_return), 2),
        "volatility": round(float(volatility), 2),
        "sharpe_ratio": round(float(sharpe_ratio), 2),
        "max_drawdown": round(float(max_drawdown), 2),
        "monthly": monthly,
        "equity": equity,
        "drawdown": drawdown,
        "prices": prices,
    }