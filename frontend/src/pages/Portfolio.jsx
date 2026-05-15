import React from 'react';
import Chart from '../components/Chart';
import Metric from '../components/Metric';
import Card from '../components/Card';
import { fmt } from '../utils/format';

export default function Portfolio({ portfolio, method, setMethod, optimizer }) {
  if (!portfolio) {
    return (
      <main className="page">
        <h1>Portfolio</h1>
        <p>Loading portfolio...</p>
      </main>
    );
  }

  return (
    <main className="page">
      <h1>Portfolio</h1>
      <p>Equal-weight multi-asset portfolio analytics</p>

      <Card title="Maximum Sharpe Portfolio">
        <div className="summary">
          <div>
            <span>Expected Return</span>
            <b>{optimizer ? `${optimizer.expected_return}%` : 'Loading...'}</b>
          </div>
          <div>
            <span>Volatility</span>
            <b>{optimizer ? `${optimizer.volatility}%` : 'Loading...'}</b>
          </div>
          <div>
            <span>Sharpe Ratio</span>
            <b className="good">{optimizer ? optimizer.sharpe_ratio : 'Loading...'}</b>
          </div>
        </div>
        <div className="weights-grid">
          {optimizer &&
            Object.entries(optimizer.weights).map(([asset, weight]) => (
              <div key={asset} className="weight-card">
                <span>{asset}</span>
                <b>{(weight * 100).toFixed(1)}%</b>
              </div>
            ))}
        </div>
      </Card>

      <select
        className="ticker-select"
        value={method}
        onChange={(e) => setMethod(e.target.value)}
      >
        <option value="equal_weight">Equal Weight</option>
        <option value="min_volatility">Minimum Volatility</option>
        <option value="max_sharpe">Maximum Sharpe</option>
        <option value="risk_parity">Risk Parity</option>
      </select>

      <div className="metrics">
        <Metric label="Total Return" value={fmt(portfolio.total_return, '%')} tone={portfolio.total_return >= 0 ? 'good' : 'bad'} />
        <Metric label="Sharpe Ratio" value={portfolio.sharpe_ratio.toFixed(2)} />
        <Metric label="Sortino Ratio" value={portfolio.sortino_ratio?.toFixed(2)} />
        <Metric label="Calmar Ratio" value={portfolio.calmar_ratio?.toFixed(2)} />
        <Metric label="Beta" value={portfolio.beta?.toFixed(2)} />
        <Metric label="VaR 95%" value={fmt(portfolio.var_95, '%')} tone="bad" />
        <Metric label="CVaR 95%" value={fmt(portfolio.cvar_95, '%')} tone="bad" />
        <Metric label="Volatility" value={`${portfolio.volatility}%`} />
        <Metric label="Max Drawdown" value={fmt(portfolio.max_drawdown, '%')} tone="bad" />
      </div>

      <div className="grid two-one">
        <Card title="Portfolio Equity Curve">
          <Chart data={portfolio.equity} />
        </Card>

        <Card title="Portfolio Weights">
          <div className="summary">
            <div>
              <span>Information Ratio</span>
              <b>{portfolio.information_ratio?.toFixed(2)}</b>
            </div>
            <div>
              <span>Tracking Error</span>
              <b>{portfolio.tracking_error?.toFixed(2)}%</b>
            </div>
            <div>
              <span>CAGR</span>
              <b>{fmt(portfolio.cagr, '%')}</b>
            </div>
            {portfolio.weights.map((w) => (
              <div key={w.ticker}>
                <span>{w.ticker}</span>
                <b>{w.weight}%</b>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </main>
  );
}
