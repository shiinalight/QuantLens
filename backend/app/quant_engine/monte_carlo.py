import numpy as np
import pandas as pd


TRADING_DAYS = 252


def simulate_gbm_paths(
    last_price: float,
    mean_return: float,
    volatility: float,
    days: int = 252,
    simulations: int = 1000,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Simulate future price paths using Geometric Brownian Motion.

    S_t = S_0 * exp((mu - 0.5*sigma^2)dt + sigma*sqrt(dt)*Z)
    """

    if last_price <= 0:
        raise ValueError("last_price must be positive")

    if days <= 0:
        raise ValueError("days must be positive")

    if simulations <= 0:
        raise ValueError("simulations must be positive")

    rng = np.random.default_rng(seed)

    dt = 1 / TRADING_DAYS
    daily_drift = (mean_return - 0.5 * volatility**2) * dt
    daily_volatility = volatility * np.sqrt(dt)

    random_shocks = rng.normal(0, 1, size=(days, simulations))
    returns = np.exp(daily_drift + daily_volatility * random_shocks)

    paths = np.zeros((days + 1, simulations))
    paths[0] = last_price
    paths[1:] = last_price * np.cumprod(returns, axis=0)

    return pd.DataFrame(paths)


def summarize_simulations(paths: pd.DataFrame) -> dict:
    """
    Summarize Monte Carlo paths using final price distribution.
    """

    final_prices = paths.iloc[-1]

    return {
        "expected_final_price": round(float(final_prices.mean()), 2),
        "median_final_price": round(float(final_prices.median()), 2),
        "worst_case_5pct": round(float(np.percentile(final_prices, 5)), 2),
        "best_case_95pct": round(float(np.percentile(final_prices, 95)), 2),
        "min_final_price": round(float(final_prices.min()), 2),
        "max_final_price": round(float(final_prices.max()), 2),
        "simulations": int(paths.shape[1]),
        "days": int(paths.shape[0] - 1),
    }


def build_monte_carlo_payload(
    last_price: float,
    mean_return: float,
    volatility: float,
    days: int = 252,
    simulations: int = 1000,
) -> dict:
    """
    Build API-ready Monte Carlo simulation payload.
    """

    paths = simulate_gbm_paths(
        last_price=last_price,
        mean_return=mean_return,
        volatility=volatility,
        days=days,
        simulations=simulations,
    )

    sample_paths = paths.iloc[:, :20]

    return {
        "summary": summarize_simulations(paths),
        "sample_paths": [
            {
                "day": int(day),
                **{
                    f"path_{col}": round(float(value), 2)
                    for col, value in row.items()
                },
            }
            for day, row in sample_paths.iterrows()
        ],
    }