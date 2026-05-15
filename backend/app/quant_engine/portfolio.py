import numpy as np
import pandas as pd
import yfinance as yf

from app.quant_engine.metrics import calculate_metrics
from scipy.optimize import minimize


def portfolio_performance(weights, mean_returns, cov_matrix):
    portfolio_return = np.sum(mean_returns * weights) * 252
    portfolio_volatility = np.sqrt(
        np.dot(weights.T, np.dot(cov_matrix * 252, weights))
    )

    sharpe = (
        portfolio_return / portfolio_volatility
        if portfolio_volatility != 0
        else 0
    )

    return portfolio_return, portfolio_volatility, sharpe


def min_volatility_weights(mean_returns, cov_matrix):
    num_assets = len(mean_returns)

    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))

    initial_weights = num_assets * [1. / num_assets]

    result = minimize(
        lambda w: portfolio_performance(w, mean_returns, cov_matrix)[1],
        initial_weights,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    return result.x


def max_sharpe_weights(mean_returns, cov_matrix):
    num_assets = len(mean_returns)

    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))

    initial_weights = num_assets * [1. / num_assets]

    result = minimize(
        lambda w: -portfolio_performance(w, mean_returns, cov_matrix)[2],
        initial_weights,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    return result.x


def risk_parity_weights(cov_matrix):
    inv_vol = 1 / np.sqrt(np.diag(cov_matrix))
    weights = inv_vol / inv_vol.sum()
    return weights


def build_optimized_portfolio(method="equal_weight", tickers=None, period="1y"):
    if tickers is None:
        tickers = ["SPY", "AAPL", "MSFT", "NVDA", "TSLA"]

    data = yf.download(tickers, period=period, auto_adjust=True, progress=False)["Close"]

    if isinstance(data, pd.Series):
        data = data.to_frame()

    returns = data.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    if method == "equal_weight":
        weights = np.ones(len(returns.columns)) / len(returns.columns)
        method_name = "Equal Weight"

    elif method == "min_volatility":
        weights = min_volatility_weights(mean_returns, cov_matrix)
        method_name = "Minimum Volatility"

    elif method == "max_sharpe":
        weights = max_sharpe_weights(mean_returns, cov_matrix)
        method_name = "Maximum Sharpe"

    elif method == "risk_parity":
        weights = risk_parity_weights(cov_matrix)
        method_name = "Risk Parity"

    else:
        raise ValueError(f"Unknown portfolio method: {method}")

    portfolio_returns = returns @ weights
    equity = (1 + portfolio_returns).cumprod() * 100

    benchmark_returns = returns["SPY"] if "SPY" in returns.columns else returns.iloc[:, 0]

    metrics = calculate_metrics(
        strategy_returns=portfolio_returns,
        benchmark_returns=benchmark_returns,
        equity=equity,
    )

    return {
        "method": method,
        "method_name": method_name,
        "tickers": list(returns.columns),
        "weights": [
            {"ticker": ticker, "weight": round(float(weight * 100), 2)}
            for ticker, weight in zip(returns.columns, weights)
        ],
        **metrics,
        "equity": [
            {"date": index.strftime("%Y-%m-%d"), "value": round(float(value), 2)}
            for index, value in equity.items()
        ],
    }


def build_equal_weight_portfolio(tickers=None, period="1y"):
    if tickers is None:
        tickers = ["SPY", "AAPL", "MSFT", "NVDA", "TSLA"]

    data = yf.download(tickers, period=period, auto_adjust=True, progress=False)["Close"]

    if isinstance(data, pd.Series):
        data = data.to_frame()

    returns = data.pct_change().dropna()
    weights = np.ones(len(returns.columns)) / len(returns.columns)

    portfolio_returns = returns @ weights
    equity = (1 + portfolio_returns).cumprod() * 100

    benchmark_returns = returns["SPY"] if "SPY" in returns.columns else returns.iloc[:, 0]

    metrics = calculate_metrics(
        strategy_returns=portfolio_returns,
        benchmark_returns=benchmark_returns,
        equity=equity,
    )

    return {
        "tickers": list(returns.columns),
        "weights": [
            {"ticker": ticker, "weight": round(float(weight * 100), 2)}
            for ticker, weight in zip(returns.columns, weights)
        ],
        **metrics,
        "equity": [
            {"date": index.strftime("%Y-%m-%d"), "value": round(float(value), 2)}
            for index, value in equity.items()
        ],
    }