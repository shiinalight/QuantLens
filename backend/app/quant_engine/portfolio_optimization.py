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