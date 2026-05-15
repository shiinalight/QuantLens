import numpy as np
import pandas as pd


def equal_weight_portfolio(
    tickers: list[str],
) -> dict[str, float]:
    """
    Create equal-weight portfolio allocation.
    """

    if not tickers:
        return {}

    weight = 1 / len(tickers)

    return {
        ticker: weight
        for ticker in tickers
    }


def portfolio_return(
    weights: np.ndarray,
    expected_returns: pd.Series,
) -> float:
    """
    Expected portfolio return.
    """

    return float(
        np.dot(weights, expected_returns)
    )


def portfolio_volatility(
    weights: np.ndarray,
    covariance_matrix: pd.DataFrame,
) -> float:
    """
    Portfolio volatility.

    sigma_p = sqrt(w^T * Cov * w)
    """

    variance = (
        weights.T
        @ covariance_matrix
        @ weights
    )

    return float(np.sqrt(variance))

TRADING_DAYS = 252


def sharpe_ratio(
    portfolio_return: float,
    portfolio_volatility: float,
    risk_free_rate: float = 0.04,
) -> float:
    """
    Sharpe Ratio.

    Measures excess return per unit of risk.
    """

    if portfolio_volatility == 0:
        return 0.0

    return (
        portfolio_return - risk_free_rate
    ) / portfolio_volatility


def optimize_max_sharpe(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    risk_free_rate: float = 0.04,
) -> dict:
    """
    Simplified maximum Sharpe allocation.

    Uses inverse volatility approximation.
    """

    volatility = np.sqrt(np.diag(covariance_matrix))

    inv_vol = 1 / volatility

    weights = inv_vol / inv_vol.sum()

    portfolio_ret = float(
        np.dot(weights, expected_returns)
    )

    portfolio_vol = float(
        np.sqrt(
            weights.T
            @ covariance_matrix.values
            @ weights
        )
    )

    sharpe = sharpe_ratio(
        portfolio_ret,
        portfolio_vol,
        risk_free_rate,
    )

    return {
        "weights": {
            asset: round(float(weight), 4)
            for asset, weight in zip(
                expected_returns.index,
                weights,
            )
        },
        "expected_return": round(portfolio_ret * 100, 2),
        "volatility": round(portfolio_vol * 100, 2),
        "sharpe_ratio": round(sharpe, 2),
    }