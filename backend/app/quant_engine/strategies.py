import numpy as np
import pandas as pd

from app.quant_engine.market_data import fetch_price_history
from app.quant_engine.metrics import calculate_metrics


def moving_average_crossover(
    ticker: str = "SPY",
    short_window: int = 20,
    long_window: int = 50,
    transaction_cost: float = 0.001,
):
    prices = fetch_price_history(ticker, period="1y")
    df = pd.DataFrame(prices)

    df["returns"] = df["close"].pct_change().fillna(0)
    df["ma_short"] = df["close"].rolling(short_window).mean()
    df["ma_long"] = df["close"].rolling(long_window).mean()

    df["signal"] = np.where(df["ma_short"] > df["ma_long"], 1, 0)
    df["position"] = df["signal"].shift(1).fillna(0)

    df["trade"] = df["position"].diff().abs().fillna(0)
    df["strategy_returns"] = (df["position"] * df["returns"]) - (df["trade"] * transaction_cost)
    turnover = df["trade"].mean() * 252 * 100
    df["equity"] = (1 + df["strategy_returns"]).cumprod() * 100
    df["benchmark_equity"] = (1 + df["returns"]).cumprod() * 100
    metrics = calculate_metrics(
        strategy_returns=df["strategy_returns"],
        benchmark_returns=df["returns"],
        equity=df["equity"],
    )

    df["rolling_max"] = df["equity"].cummax()
    df["drawdown"] = (df["equity"] / df["rolling_max"] - 1) * 100

    total_return = df["equity"].iloc[-1] - 100
    benchmark_return = df["benchmark_equity"].iloc[-1] - 100
    excess_return = total_return - benchmark_return

    return {
        "name": f"MA {short_window}/{long_window} Crossover",
        "ticker": ticker,
        **metrics,
        "benchmark_return": round(float(benchmark_return), 2),
        "excess_return": round(float(excess_return), 2),
        "turnover": round(float(turnover), 2),
        "transaction_cost": transaction_cost,
        "equity": [
            {"date": row["date"], "value": round(float(row["equity"]), 2)}
            for _, row in df.iterrows()
        ],
        "benchmark": [
            {"date": row["date"], "value": round(float(row["benchmark_equity"]), 2)}
            for _, row in df.iterrows()
        ],
        "signal": [
            {
                "date": row["date"],
                "close": round(float(row["close"]), 2),
                "ma_short": None if pd.isna(row["ma_short"]) else round(float(row["ma_short"]), 2),
                "ma_long": None if pd.isna(row["ma_long"]) else round(float(row["ma_long"]), 2),
                "position": int(row["position"]),
            }
            for _, row in df.iterrows()
        ],
    }


def mean_reversion(ticker: str = "SPY", lookback: int = 5):
    prices = fetch_price_history(ticker, period="1y")
    df = pd.DataFrame(prices)

    df["returns"] = df["close"].pct_change().fillna(0)

    # If recent return is negative, expect reversal upward.
    df["rolling_return"] = df["close"].pct_change(lookback)
    df["signal"] = np.where(df["rolling_return"] < 0, 1, 0)
    df["position"] = df["signal"].shift(1).fillna(0)

    df["trade"] = df["position"].diff().abs().fillna(0)
    transaction_cost = 0.001
    df["strategy_returns"] = (df["position"] * df["returns"]) - (df["trade"] * transaction_cost)
    turnover = df["trade"].mean() * 252 * 100

    df["equity"] = (1 + df["strategy_returns"]).cumprod() * 100
    df["benchmark_equity"] = (1 + df["returns"]).cumprod() * 100
    metrics = calculate_metrics(
        strategy_returns=df["strategy_returns"],
        benchmark_returns=df["returns"],
        equity=df["equity"],
    )
    df["rolling_max"] = df["equity"].cummax()
    df["drawdown"] = (df["equity"] / df["rolling_max"] - 1) * 100

    total_return = df["equity"].iloc[-1] - 100
    benchmark_return = df["benchmark_equity"].iloc[-1] - 100
    excess_return = total_return - benchmark_return

    return {
        "name": f"Mean Reversion {lookback}D",
        "ticker": ticker,
        **metrics,
        "benchmark_return": round(float(benchmark_return), 2),
        "excess_return": round(float(excess_return), 2),
        "turnover": round(float(turnover), 2),
        "transaction_cost": transaction_cost,
        "equity": [
            {"date": row["date"], "value": round(float(row["equity"]), 2)}
            for _, row in df.iterrows()
        ],
        "benchmark": [
            {"date": row["date"], "value": round(float(row["benchmark_equity"]), 2)}
            for _, row in df.iterrows()
        ],
        "signal": [
            {
                "date": row["date"],
                "close": round(float(row["close"]), 2),
                "rolling_return": None if pd.isna(row["rolling_return"]) else round(float(row["rolling_return"]), 4),
                "position": int(row["position"]),
            }
            for _, row in df.iterrows()
        ],
    }


def momentum(ticker: str = "SPY", lookback: int = 20):
    prices = fetch_price_history(ticker, period="1y")
    df = pd.DataFrame(prices)

    df["returns"] = df["close"].pct_change().fillna(0)
    df["momentum"] = df["close"].pct_change(lookback)

    df["signal"] = np.where(df["momentum"] > 0, 1, 0)
    df["position"] = df["signal"].shift(1).fillna(0)

    df["trade"] = df["position"].diff().abs().fillna(0)
    transaction_cost = 0.001
    df["strategy_returns"] = (df["position"] * df["returns"]) - (df["trade"] * transaction_cost)
    turnover = df["trade"].mean() * 252 * 100

    df["equity"] = (1 + df["strategy_returns"]).cumprod() * 100
    df["benchmark_equity"] = (1 + df["returns"]).cumprod() * 100
    metrics = calculate_metrics(
        strategy_returns=df["strategy_returns"],
        benchmark_returns=df["returns"],
        equity=df["equity"],
    )
    df["rolling_max"] = df["equity"].cummax()
    df["drawdown"] = (df["equity"] / df["rolling_max"] - 1) * 100

    total_return = df["equity"].iloc[-1] - 100
    benchmark_return = df["benchmark_equity"].iloc[-1] - 100
    excess_return = total_return - benchmark_return

    return {
        "name": f"Momentum {lookback}D",
        "ticker": ticker,
        **metrics,
        "benchmark_return": round(float(benchmark_return), 2),
        "excess_return": round(float(excess_return), 2),
        "turnover": round(float(turnover), 2),
        "transaction_cost": transaction_cost,
        "equity": [
            {"date": row["date"], "value": round(float(row["equity"]), 2)}
            for _, row in df.iterrows()
        ],
        "benchmark": [
            {"date": row["date"], "value": round(float(row["benchmark_equity"]), 2)}
            for _, row in df.iterrows()
        ],
        "signal": [
            {
                "date": row["date"],
                "close": round(float(row["close"]), 2),
                "momentum": None if pd.isna(row["momentum"]) else round(float(row["momentum"]), 4),
                "position": int(row["position"]),
            }
            for _, row in df.iterrows()
        ],
    }
def volatility_breakout(ticker: str = "SPY", lookback: int = 20):
    prices = fetch_price_history(ticker, period="1y")
    df = pd.DataFrame(prices)

    df["returns"] = df["close"].pct_change().fillna(0)
    df["volatility"] = df["returns"].rolling(lookback).std()
    df["volatility_threshold"] = df["volatility"].rolling(lookback).mean()

    df["signal"] = np.where(df["volatility"] > df["volatility_threshold"], 1, 0)
    df["position"] = df["signal"].shift(1).fillna(0)

    df["trade"] = df["position"].diff().abs().fillna(0)
    transaction_cost = 0.001
    df["strategy_returns"] = (df["position"] * df["returns"]) - (df["trade"] * transaction_cost)
    turnover = df["trade"].mean() * 252 * 100

    df["equity"] = (1 + df["strategy_returns"]).cumprod() * 100
    df["benchmark_equity"] = (1 + df["returns"]).cumprod() * 100
    metrics = calculate_metrics(
        strategy_returns=df["strategy_returns"],
        benchmark_returns=df["returns"],
        equity=df["equity"],
    )
    df["rolling_max"] = df["equity"].cummax()
    df["drawdown"] = (df["equity"] / df["rolling_max"] - 1) * 100

    total_return = df["equity"].iloc[-1] - 100
    benchmark_return = df["benchmark_equity"].iloc[-1] - 100
    excess_return = total_return - benchmark_return

    return {
        "name": f"Volatility Breakout {lookback}D",
        "ticker": ticker,
        **metrics,
        "benchmark_return": round(float(benchmark_return), 2),
        "excess_return": round(float(excess_return), 2),
        "turnover": round(float(turnover), 2),
        "transaction_cost": transaction_cost,
        "equity": [
            {"date": row["date"], "value": round(float(row["equity"]), 2)}
            for _, row in df.iterrows()
        ],
        "benchmark": [
            {"date": row["date"], "value": round(float(row["benchmark_equity"]), 2)}
            for _, row in df.iterrows()
        ],
        "signal": [
            {
                "date": row["date"],
                "close": round(float(row["close"]), 2),
                "volatility": None if pd.isna(row["volatility"]) else round(float(row["volatility"]), 4),
                "volatility_threshold": None if pd.isna(row["volatility_threshold"]) else round(float(row["volatility_threshold"]), 4),
                "position": int(row["position"]),
            }
            for _, row in df.iterrows()
        ],
    }