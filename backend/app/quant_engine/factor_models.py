import pandas as pd


def capm_expected_return(
    risk_free_rate: float,
    beta_value: float,
    market_return: float,
) -> float:
    """
    Capital Asset Pricing Model.

    E(R_i) = R_f + beta_i * (E(R_m) - R_f)
    """

    return (
        risk_free_rate
        + beta_value * (market_return - risk_free_rate)
    )


def calculate_alpha(
    asset_return: float,
    expected_return: float,
) -> float:
    """
    Jensen's Alpha.

    alpha = actual return - expected return
    """

    return asset_return - expected_return


def rolling_beta(
    asset_returns: pd.Series,
    benchmark_returns: pd.Series,
    window: int = 60,
) -> pd.Series:
    """
    Rolling beta calculation.
    """

    covariance = (
        asset_returns.rolling(window)
        .cov(benchmark_returns)
    )

    variance = benchmark_returns.rolling(window).var()

    return covariance / variance