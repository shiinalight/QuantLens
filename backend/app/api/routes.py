from fastapi import APIRouter
from pydantic import BaseModel
from app.quant_engine.demo_data import build_demo_payload
from app.quant_engine.backtester import run_backtest
from app.quant_engine.alpha_executor import run_alpha_formula
from app.quant_engine.market_data import build_market_payload
from app.quant_engine.strategies import (
    moving_average_crossover,
    mean_reversion,
    momentum,
    volatility_breakout,
)
from app.quant_engine.market_overview import build_market_overview
from app.quant_engine.portfolio import build_equal_weight_portfolio, build_optimized_portfolio


router = APIRouter()


class AlphaRequest(BaseModel):
    ticker: str = "SPY"
    formula: str = "rolling_mean(close, 20) > rolling_mean(close, 50)"
    transaction_cost: float = 0.001


@router.get("/demo")
def demo():
    return build_demo_payload()


@router.get("/market/{ticker}")
def market(ticker: str):
    return build_market_payload(ticker.upper())


@router.post("/backtest")
def backtest(alpha_formula: str = "rank(vwap / close) - rank(volume / adv20) + ts_rank(returns, 10)"):
    return run_backtest(alpha_formula)


@router.post("/alpha/run")
def run_alpha(request: AlphaRequest):
    return run_alpha_formula(
        ticker=request.ticker.upper(),
        formula=request.formula,
        transaction_cost=request.transaction_cost,
    )

@router.get("/strategy/ma-crossover/{ticker}")
def ma_crossover(
    ticker: str,
    short_window: int = 20,
    long_window: int = 50,
    transaction_cost: float = 0.001,
):
    return moving_average_crossover(
        ticker=ticker.upper(),
        short_window=short_window,
        long_window=long_window,
        transaction_cost=transaction_cost,
    )

@router.get("/strategy/mean-reversion/{ticker}")
def mean_reversion_strategy(ticker: str):
    return mean_reversion(ticker.upper())

@router.get("/strategy/momentum/{ticker}")
def momentum_strategy(ticker: str):
    return momentum(ticker.upper())

@router.get("/strategy/volatility-breakout/{ticker}")
def volatility_breakout_strategy(ticker: str):
    return volatility_breakout(ticker.upper())

@router.get("/market-overview")
def market_overview():
    return build_market_overview()

@router.get("/portfolio/equal-weight")
def equal_weight_portfolio():
    return build_equal_weight_portfolio()


@router.get("/portfolio/{method}")
def optimized_portfolio(method: str):
    return build_optimized_portfolio(method)