import pandas as pd

from app.quant_engine.market_data import fetch_price_history
from app.quant_engine.risk_models import (
    calculate_returns,
    calculate_log_returns,
    annualized_volatility,
    historical_var,
    historical_cvar,
    max_drawdown,
)
from app.quant_engine.factor_models import capm_expected_return
from app.quant_engine.timeframes import apply_timeframe


def _to_period(timeframe: str) -> str:
    mapping = {
        "1M": "1mo",
        "3M": "3mo",
        "6M": "6mo",
        "1Y": "1y",
        "3Y": "3y",
        "5Y": "5y",
    }
    return mapping.get(timeframe.upper(), "1y")


def build_quant_analytics_payload(ticker: str = "SPY", timeframe: str = "1Y"):
    prices = fetch_price_history(ticker, period=_to_period(timeframe))

    df = pd.DataFrame(prices)
    df = apply_timeframe(df, timeframe)
    price_series = df["close"]

    returns = calculate_returns(price_series)
    log_returns = calculate_log_returns(price_series)

    total_return = (price_series.iloc[-1] / price_series.iloc[0] - 1) * 100
    ann_vol = annualized_volatility(returns) * 100
    var_95 = historical_var(returns, 0.95) * 100
    cvar_95 = historical_cvar(returns, 0.95) * 100
    mdd = max_drawdown(price_series) * 100

    risk_free_rate = 0.04
    beta_value = 1.0
    market_return = 0.10
    capm_return = capm_expected_return(
        risk_free_rate=risk_free_rate,
        beta_value=beta_value,
        market_return=market_return,
    ) * 100

    return {
        "ticker": ticker,
        "timeframe": timeframe.upper(),
        "total_return": round(float(total_return), 2),
        "annualized_volatility": round(float(ann_vol), 2),
        "value_at_risk_95": round(float(var_95), 2),
        "conditional_var_95": round(float(cvar_95), 2),
        "max_drawdown": round(float(mdd), 2),
        "capm_expected_return": round(float(capm_return), 2),
        "risk_free_rate": round(risk_free_rate * 100, 2),
        "assumed_beta": beta_value,
        "assumed_market_return": round(market_return * 100, 2),
        "observations": len(returns),
        "latest_log_return": round(float(log_returns.iloc[-1] * 100), 2),
    }