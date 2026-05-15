import React from 'react';
import Card from '../components/Card';

export default function SettingsPage({ ticker }) {
  return (
    <main className="page">
      <h1>Settings</h1>
      <p>Current QuantLens configuration</p>

      <div className="grid two">
        <Card title="Data Configuration">
          <div className="summary">
            <div><span>Primary Ticker</span><b>{ticker}</b></div>
            <div><span>Data Source</span><b>Yahoo Finance via yfinance</b></div>
            <div><span>Lookback Window</span><b>1 Year</b></div>
            <div><span>Frequency</span><b>Daily</b></div>
          </div>
        </Card>

        <Card title="Backtest Assumptions">
          <div className="summary">
            <div><span>Transaction Cost</span><b>0.10%</b></div>
            <div><span>Position Type</span><b>Long / Cash</b></div>
            <div><span>Benchmark</span><b>Buy & Hold</b></div>
            <div><span>Annualization</span><b>252 Trading Days</b></div>
          </div>
        </Card>
      </div>
    </main>
  );
}
