import React from 'react';
import { ComparisonChart } from '../components/Chart';
import Metric from '../components/Metric';
import Card from '../components/Card';
import { fmt } from '../utils/format';

export default function StrategyExplorer({ strategies, strategyParams, setStrategyParams }) {
  return (
    <main className="page">
      <h1>Strategy Explorer</h1>
      <p>Backtest and compare trading strategies</p>
      <div className="controls">
        <label>
          Short MA
          <input
            type="number"
            value={strategyParams.shortWindow}
            onChange={(e) =>
              setStrategyParams({ ...strategyParams, shortWindow: Number(e.target.value) })
            }
          />
        </label>

        <label>
          Long MA
          <input
            type="number"
            value={strategyParams.longWindow}
            onChange={(e) =>
              setStrategyParams({ ...strategyParams, longWindow: Number(e.target.value) })
            }
          />
        </label>

        <label>
          Transaction Cost
          <input
            type="number"
            step="0.0001"
            value={strategyParams.transactionCost}
            onChange={(e) =>
              setStrategyParams({ ...strategyParams, transactionCost: Number(e.target.value) })
            }
          />
        </label>
      </div>
      <div className="strategy-grid">
        {strategies.map((s) => (
          <div className="strategy" key={s.name}>
            <h3>{s.name}</h3>
            <small>{s.category}</small>
            <div className="triple">
              <Metric label="Return" value={fmt(s.return, '%')} tone={s.return >= 0 ? 'good' : 'bad'} />
              <Metric
                label="Alpha"
                value={fmt(s.alpha, '%')}
                tone={s.alpha >= 0 ? 'good' : 'bad'}
              />
              <Metric label="Sharpe" value={s.sharpe.toFixed(2)} />
              <Metric label="Drawdown" value={fmt(s.drawdown, '%')} tone="bad" />
            </div>
            <ComparisonChart strategy={s.curve} benchmark={s.benchmark} />
          </div>
        ))}
      </div>
      <Card title="Strategy Comparison">
        <table>
          <tbody>
            {strategies.map((s) => (
              <tr key={s.name}>
                <td>{s.name}</td>
                <td className="good">{fmt(s.return, '%')}</td>
                <td>{s.sharpe.toFixed(2)}</td>
                <td className="bad">{fmt(s.drawdown, '%')}</td>
                <td>{s.turnover.toFixed(1)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </main>
  );
}
