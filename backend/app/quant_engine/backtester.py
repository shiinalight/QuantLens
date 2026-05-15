import numpy as np
import pandas as pd

TRADING_DAYS = 252


def sharpe_ratio(returns: pd.Series) -> float:
    return float(np.sqrt(TRADING_DAYS) * returns.mean() / (returns.std() + 1e-12))


def sortino_ratio(returns: pd.Series) -> float:
    downside = returns[returns < 0].std()
    return float(np.sqrt(TRADING_DAYS) * returns.mean() / (downside + 1e-12))


def max_drawdown(equity: pd.Series) -> float:
    peak = equity.cummax()
    dd = equity / peak - 1
    return float(dd.min())


def turnover(weights: pd.Series) -> float:
    return float(weights.diff().abs().mean())


def run_backtest(alpha_formula: str):
    """Educational vectorized backtest scaffold.

    Current implementation uses synthetic OHLCV-like data so the repo runs immediately.
    Next milestone: plug in yfinance/polygon data and parse a safer alpha DSL.
    """
    rng = np.random.default_rng(123)
    dates = pd.date_range("2023-01-01", periods=252, freq="B")
    returns = pd.Series(rng.normal(0.0007, 0.012, len(dates)), index=dates)
    raw_signal = -returns.rolling(5).mean().fillna(0) + returns.rolling(20).mean().fillna(0)
    weights = raw_signal.rank(pct=True) - 0.5
    strategy_returns = weights.shift(1).fillna(0) * returns
    equity = (1 + strategy_returns).cumprod()
    return {
        "alpha_formula": alpha_formula,
        "metrics": {
            "total_return": float(equity.iloc[-1] - 1),
            "sharpe": sharpe_ratio(strategy_returns),
            "sortino": sortino_ratio(strategy_returns),
            "max_drawdown": max_drawdown(equity),
            "turnover": turnover(weights),
        },
        "equity": [{"date": str(k.date()), "value": float(v)} for k, v in equity.items()],
    }
