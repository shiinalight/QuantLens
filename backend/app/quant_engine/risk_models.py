import numpy as np
import pandas as pd


TRADING_DAYS = 252


def calculate_returns(prices: pd.Series) -> pd.Series:
    """
    Calculate simple percentage returns.

    Formula:
    r_t = (P_t / P_{t-1}) - 1
    """
    return prices.pct_change().dropna()


def calculate_log_returns(prices: pd.Series) -> pd.Series:
    """
    Calculate logarithmic returns.

    Formula:
    r_t = ln(P_t / P_{t-1})
    """
    return np.log(prices / prices.shift(1)).dropna()


def annualized_volatility(
    returns: pd.Series,
    periods_per_year: int = TRADING_DAYS,
) -> float:
    """
    Annualized volatility.

    sigma_annual = sigma_daily * sqrt(252)
    """
    return float(returns.std() * np.sqrt(periods_per_year))


def historical_var(
    returns: pd.Series,
    confidence_level: float = 0.95,
) -> float:
    """
    Historical Value at Risk (VaR).

    Example:
    VaR = -2.5% at 95% confidence
    means only 5% of days are expected
    to lose more than 2.5%.
    """
    alpha = 1 - confidence_level
    return float(np.percentile(returns.dropna(), alpha * 100))


def historical_cvar(
    returns: pd.Series,
    confidence_level: float = 0.95,
) -> float:
    """
    Conditional Value at Risk (CVaR).

    Average loss beyond VaR.
    """
    var = historical_var(returns, confidence_level)
    tail_losses = returns[returns <= var]

    return float(tail_losses.mean())


def max_drawdown(prices: pd.Series) -> float:
    """
    Maximum portfolio drawdown.

    Measures worst peak-to-trough decline.
    """
    running_max = prices.cummax()
    drawdown = prices / running_max - 1

    return float(drawdown.min())


def beta(
    asset_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> float:
    """
    CAPM Beta.

    beta = Cov(R_i, R_m) / Var(R_m)
    """
    aligned = pd.concat(
        [asset_returns, benchmark_returns],
        axis=1,
    ).dropna()

    aligned.columns = ["asset", "benchmark"]

    covariance = aligned["asset"].cov(aligned["benchmark"])
    benchmark_variance = aligned["benchmark"].var()

    if benchmark_variance == 0:
        return 0.0

    return float(covariance / benchmark_variance)