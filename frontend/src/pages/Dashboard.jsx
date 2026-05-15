import React from 'react';
import Chart, { Bars, Drawdown } from '../components/Chart';
import Metric from '../components/Metric';
import Card from '../components/Card';
import { fmt } from '../utils/format';

function Summary({ data }) {
  const market = data.market;

  const rows = market
    ? [
        ['Ticker', market.ticker, ''],
        ['Last Price', `$${market.price}`, ''],
        ['Total Return', fmt(market.total_return, '%'), market.total_return >= 0 ? 'good' : 'bad'],
        ['Sharpe Ratio', market.sharpe_ratio.toFixed(2), ''],
        ['Max Drawdown', fmt(market.max_drawdown, '%'), 'bad'],
        ['Volatility', `${market.volatility}%`, ''],
      ]
    : [['Loading', 'Fetching market data...', '']];

  return (
    <div className="summary">
      {rows.map(([a, b, c]) => (
        <div key={a}>
          <span>{a}</span>
          <b className={c}>{b}</b>
        </div>
      ))}
    </div>
  );
}

export default function Dashboard({ data }) {
  return (
    <main className="page">
      <h1>Dashboard</h1>
      <p>Your quantitative overview</p>
      <div className="metrics">
        <Metric
          label="Total Return"
          value={data.market ? fmt(data.market.total_return, '%') : 'Loading...'}
          tone={data.market?.total_return >= 0 ? 'good' : 'bad'}
        />
        <Metric
          label="Sharpe Ratio"
          value={data.market ? data.market.sharpe_ratio.toFixed(2) : 'Loading...'}
        />
        <Metric
          label="Max Drawdown"
          value={data.market ? fmt(data.market.max_drawdown, '%') : 'Loading...'}
          tone="bad"
        />
        <Metric
          label="Volatility"
          value={data.market ? `${data.market.volatility}%` : 'Loading...'}
        />
        <Metric
          label="Price"
          value={data.market ? `$${data.market.price}` : 'Loading...'}
        />
      </div>
      <div className="grid two-one">
        <Card title="Equity Curve"><Chart data={data.equity} /></Card>
        <Card title="Performance Summary"><Summary data={data} /></Card>
      </div>
      <div className="grid two">
        <Card title="Monthly Returns"><Bars data={data.monthly} /></Card>
        <Card title="Drawdown"><Drawdown data={data.drawdown} /></Card>
      </div>
    </main>
  );
}
