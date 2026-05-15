import React, { useState } from 'react';
import Chart, { SignalPreviewChart } from '../components/Chart';
import Card from '../components/Card';
import { fmt } from '../utils/format';
import { runAlpha } from '../services/api';

export default function AlphaLab({ data }) {
  const [formula, setFormula] = useState('rolling_mean(close, 20) > rolling_mean(close, 50)');
  const [alphaResult, setAlphaResult] = useState(data.liveStrategy);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [transactionCost, setTransactionCost] = useState(0.001);
  const activeAlpha = alphaResult || data.liveStrategy;

  async function handleRunAlpha() {
    setLoading(true);
    setError('');
    try {
      const result = await runAlpha({
        ticker: data.market?.ticker || 'SPY',
        formula,
        transaction_cost: transactionCost,
      });
      setAlphaResult(result);
    } catch (err) {
      setError(err?.message || 'Failed to run alpha formula');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <h1>Alpha Lab</h1>
      <p>Create, test, and explain alpha signals</p>
      <div className="grid two">
        <Card title="Alpha Formula">
          <textarea
            className="alpha-input"
            value={formula}
            onChange={(e) => setFormula(e.target.value)}
          />
          <button className="primary" onClick={handleRunAlpha} disabled={loading}>
            {loading ? 'Running...' : 'Run Alpha'}
          </button>
          {error && <p className="bad">{error}</p>}
          <button onClick={() => setShowSettings(!showSettings)}>
            Settings
          </button>
          {showSettings && (
            <div className="alpha-settings">
              <label>
                Transaction Cost
                <input
                  type="number"
                  step="0.0001"
                  min="0"
                  value={transactionCost}
                  onChange={(e) => setTransactionCost(Number(e.target.value))}
                />
              </label>

              <small>
                Example: 0.001 = 0.10% per trade
              </small>
            </div>
          )}
        </Card>
        <Card title="Signal Preview">
          <SignalPreviewChart data={activeAlpha?.signal || data.signal} />
        </Card>
      </div>
      <div className="grid two">
        <Card title="Backtest Performance">
          <Chart data={activeAlpha?.equity || data.equity} />
        </Card>
        <Card title="Strategy Diagnostics">
          <div className="summary">
            <div>
              <span>Ticker</span>
              <b>{activeAlpha?.ticker || 'Loading...'}</b>
            </div>
            <div>
              <span>Transaction Cost</span>
              <b>{activeAlpha ? `${(activeAlpha.transaction_cost * 100).toFixed(2)}%` : 'Loading...'}</b>
            </div>
            <div>
              <span>Turnover</span>
              <b>{activeAlpha ? `${activeAlpha.turnover}%` : 'Loading...'}</b>
            </div>
            <div>
              <span>Strategy Return</span>
              <b className={activeAlpha?.total_return >= 0 ? 'good' : 'bad'}>
                {activeAlpha ? fmt(activeAlpha.total_return, '%') : 'Loading...'}
              </b>
            </div>
            <div>
              <span>Benchmark Return</span>
              <b>{activeAlpha ? fmt(activeAlpha.benchmark_return, '%') : 'Loading...'}</b>
            </div>
            <div>
              <span>Alpha</span>
              <b className={activeAlpha?.excess_return >= 0 ? 'good' : 'bad'}>
                {activeAlpha ? fmt(activeAlpha.excess_return, '%') : 'Loading...'}
              </b>
            </div>
            <div>
              <span>Sortino Ratio</span>
              <b>{activeAlpha ? activeAlpha.sortino_ratio?.toFixed(2) : 'Loading...'}</b>
            </div>
            <div>
              <span>Information Ratio</span>
              <b>{activeAlpha ? activeAlpha.information_ratio?.toFixed(2) : 'Loading...'}</b>
            </div>
            <div>
              <span>Beta</span>
              <b>{activeAlpha ? activeAlpha.beta?.toFixed(2) : 'Loading...'}</b>
            </div>
            <div>
              <span>VaR 95%</span>
              <b className="bad">{activeAlpha ? fmt(activeAlpha.var_95, '%') : 'Loading...'}</b>
            </div>
            <div>
              <span>CVaR 95%</span>
              <b className="bad">{activeAlpha ? fmt(activeAlpha.cvar_95, '%') : 'Loading...'}</b>
            </div>
          </div>
        </Card>
      </div>
    </main>
  );
}
