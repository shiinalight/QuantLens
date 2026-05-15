import React from 'react';
import Card from '../components/Card';
import { fmt } from '../utils/format';

export default function Backtests({ strategies }) {
  return (
    <main className="page">
      <h1>Backtests</h1>
      <p>Real strategy backtest comparison with transaction costs and benchmark alpha</p>

      <Card title="Backtest Results">
        <table>
          <thead>
            <tr>
              <th>Strategy</th>
              <th>Category</th>
              <th>Return</th>
              <th>Alpha</th>
              <th>Sharpe</th>
              <th>Sortino</th>
              <th>Info Ratio</th>
              <th>Beta</th>
              <th>VaR 95%</th>
              <th>CVaR 95%</th>
              <th>Drawdown</th>
              <th>Turnover</th>
            </tr>
          </thead>
          <tbody>
            {strategies.map((s) => (
              <tr key={s.name}>
                <td>{s.name}</td>
                <td>{s.category}</td>
                <td className={s.return >= 0 ? 'good' : 'bad'}>{fmt(s.return, '%')}</td>
                <td className={s.alpha >= 0 ? 'good' : 'bad'}>{fmt(s.alpha, '%')}</td>
                <td>{s.sharpe.toFixed(2)}</td>
                <td>{s.sortino?.toFixed(2)}</td>
                <td>{s.infoRatio?.toFixed(2)}</td>
                <td>{s.beta?.toFixed(2)}</td>
                <td className="bad">{fmt(s.var95, '%')}</td>
                <td className="bad">{fmt(s.cvar95, '%')}</td>
                <td className="bad">{fmt(s.drawdown, '%')}</td>
                <td>{s.turnover.toFixed(2)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </main>
  );
}
