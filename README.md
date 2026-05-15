# QuantLens

QuantLens is a full-stack quantitative research dashboard built with FastAPI and React.
It combines live market data, multi-strategy backtesting, custom alpha execution, advanced risk metrics, market scanners, and portfolio optimization in one interface.

## Tech Stack

- Backend: FastAPI, pandas, numpy, scipy, yfinance
- Frontend: React, Vite, Recharts, lucide-react
- Data: Yahoo Finance via yfinance

## Core Features

- Multi-strategy backtests
  - Moving Average Crossover (parameterized short/long windows and transaction cost)
  - Mean Reversion
  - Momentum
  - Volatility Breakout
- Shared advanced metrics across strategies and portfolio
  - Total Return, Volatility, Sharpe, Sortino, Calmar, Max Drawdown
  - Information Ratio, Tracking Error, Beta, VaR 95%, CVaR 95%, CAGR
  - Benchmark Return and Excess Return (Alpha)
- Alpha Lab
  - Run custom formula-driven strategies from the UI
  - Configure transaction costs
  - Inspect diagnostics and signal preview
- Market View scanners
  - Heatmap
  - Volume Spikes
  - Top Gainers / Top Losers
  - Rolling Volatility Scanner
  - Relative Strength (5-day)
- Portfolio optimization modes
  - Equal Weight
  - Minimum Volatility
  - Maximum Sharpe
  - Risk Parity

## Project Structure

```txt
quantlens/
	backend/
		app/
			api/
			quant_engine/
	frontend/
		src/
			components/
			pages/
			services/
	docs/
	notebooks/
```

## Local Setup

### 1) Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend URL:

```txt
http://127.0.0.1:8000
```

### 2) Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```txt
http://127.0.0.1:5173
```

## API Overview

All API routes are served under:

```txt
/api
```

Key endpoints:

- GET /api/demo
- GET /api/market/{ticker}
- GET /api/market-overview
- POST /api/backtest
- POST /api/alpha/run
- GET /api/strategy/ma-crossover/{ticker}
  - Query params: short_window, long_window, transaction_cost
- GET /api/strategy/mean-reversion/{ticker}
- GET /api/strategy/momentum/{ticker}
- GET /api/strategy/volatility-breakout/{ticker}
- GET /api/portfolio/equal-weight
- GET /api/portfolio/{method}
  - method values: equal_weight, min_volatility, max_sharpe, risk_parity

## Frontend Pages

- Dashboard: market performance snapshot, equity, drawdown, monthly returns
- Strategy Explorer: strategy cards, benchmark comparison, MA parameter controls
- Alpha Lab: formula execution, diagnostics, and signal preview chart
- Market View: heatmap and ranked scanner tables
- Portfolio: optimization method selector, risk/performance cards, weight breakdown
- Backtests: cross-strategy table with advanced metrics
- News and Sentiment: market-overview-driven movers and sentiment proxy
- Settings: project assumptions and configuration summary

## Notes

- If your editor reports unresolved imports for installed Python packages (for example yfinance), ensure VS Code is using the backend virtual environment interpreter.
- Transaction cost is represented as a decimal (example: 0.001 = 0.10% per trade).
- This project is for educational and research use only, not investment advice.
