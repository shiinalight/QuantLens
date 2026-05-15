import numpy as np
import pandas as pd


def calculate_metrics(strategy_returns, benchmark_returns=None, equity=None):
    strategy_returns = pd.Series(strategy_returns).fillna(0)

    if benchmark_returns is None:
        benchmark_returns = pd.Series([0] * len(strategy_returns))
    else:
        benchmark_returns = pd.Series(benchmark_returns).fillna(0)

    if equity is None:
        equity = (1 + strategy_returns).cumprod() * 100
    else:
        equity = pd.Series(equity).fillna(method="ffill")

    rolling_max = equity.cummax()
    drawdown = (equity / rolling_max - 1) * 100

    total_return = equity.iloc[-1] - 100
    volatility = strategy_returns.std() * np.sqrt(252) * 100

    sharpe = (
        strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
        if strategy_returns.std() != 0
        else 0
    )

    downside_returns = strategy_returns[strategy_returns < 0]
    downside_volatility = downside_returns.std() * np.sqrt(252)

    sortino = (
        strategy_returns.mean() / downside_returns.std() * np.sqrt(252)
        if downside_returns.std() != 0
        else 0
    )

    max_drawdown = drawdown.min()
    cagr = ((equity.iloc[-1] / equity.iloc[0]) ** (252 / len(equity)) - 1) * 100

    calmar = (
        cagr / abs(max_drawdown)
        if max_drawdown != 0
        else 0
    )

    active_returns = strategy_returns - benchmark_returns
    tracking_error = active_returns.std() * np.sqrt(252) * 100

    information_ratio = (
        active_returns.mean() / active_returns.std() * np.sqrt(252)
        if active_returns.std() != 0
        else 0
    )

    beta = (
        strategy_returns.cov(benchmark_returns) / benchmark_returns.var()
        if benchmark_returns.var() != 0
        else 0
    )

    var_95 = np.percentile(strategy_returns, 5) * 100
    cvar_95 = strategy_returns[strategy_returns <= np.percentile(strategy_returns, 5)].mean() * 100

    return {
        "total_return": round(float(total_return), 2),
        "volatility": round(float(volatility), 2),
        "sharpe_ratio": round(float(sharpe), 2),
        "sortino_ratio": round(float(sortino), 2),
        "max_drawdown": round(float(max_drawdown), 2),
        "cagr": round(float(cagr), 2),
        "calmar_ratio": round(float(calmar), 2),
        "tracking_error": round(float(tracking_error), 2),
        "information_ratio": round(float(information_ratio), 2),
        "beta": round(float(beta), 2),
        "var_95": round(float(var_95), 2),
        "cvar_95": round(float(cvar_95), 2),
    }