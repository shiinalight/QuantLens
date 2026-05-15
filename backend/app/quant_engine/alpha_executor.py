import numpy as np
import pandas as pd

from app.quant_engine.market_data import fetch_price_history
from app.quant_engine.metrics import calculate_metrics


def run_alpha_formula(
    ticker: str = "SPY",
    formula: str = "rolling_mean(close, 20) > rolling_mean(close, 50)",
    transaction_cost: float = 0.001,
):
    prices = fetch_price_history(ticker, period="1y")
    df = pd.DataFrame(prices)

    df["returns"] = df["close"].pct_change().fillna(0)

    allowed_context = {
        "close": df["close"],
        "returns": df["returns"],
        "rolling_mean": lambda series, window: series.rolling(int(window)).mean(),
        "rolling_std": lambda series, window: series.rolling(int(window)).std(),
        "pct_change": lambda series, window: series.pct_change(int(window)),
        "np": np,
    }

    try:
        signal_raw = eval(formula, {"__builtins__": {}}, allowed_context)
    except Exception as error:
        raise ValueError(f"Invalid alpha formula: {error}")

    df["signal"] = np.where(signal_raw, 1, 0)
    df["position"] = df["signal"].shift(1).fillna(0)

    df["trade"] = df["position"].diff().abs().fillna(0)
    df["strategy_returns"] = (df["position"] * df["returns"]) - (df["trade"] * transaction_cost)

    df["equity"] = (1 + df["strategy_returns"]).cumprod() * 100
    df["benchmark_equity"] = (1 + df["returns"]).cumprod() * 100

    df["rolling_max"] = df["equity"].cummax()
    df["drawdown"] = (df["equity"] / df["rolling_max"] - 1) * 100

    total_return = df["equity"].iloc[-1] - 100
    benchmark_return = df["benchmark_equity"].iloc[-1] - 100
    excess_return = total_return - benchmark_return

    turnover = df["trade"].mean() * 252 * 100
    metrics = calculate_metrics(
        strategy_returns=df["strategy_returns"],
        benchmark_returns=df["returns"],
        equity=df["equity"],
    )

    return {
        "name": "Custom Alpha",
        "ticker": ticker,
        "formula": formula,
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
                "position": int(row["position"]),
            }
            for _, row in df.iterrows()
        ],
    }