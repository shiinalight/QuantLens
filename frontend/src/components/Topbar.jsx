import React from 'react';

export default function Topbar({ ticker, setTicker, timeframe, setTimeframe, page, setPage }) {
  const showTicker = ['Dashboard', 'Strategy Explorer', 'Alpha Lab', 'Market View'].includes(page);

  return (
    <header className="topbar">
      <div></div>

      <div className="filters">
        {showTicker && (
          <select
            className="ticker-select"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
          >
            <option value="SPY">SPY</option>
            <option value="AAPL">AAPL</option>
            <option value="MSFT">MSFT</option>
            <option value="NVDA">NVDA</option>
            <option value="TSLA">TSLA</option>
            <option value="BTC-USD">BTC-USD</option>
          </select>
        )}

        {showTicker && (
          <select
            className="timeframe-select"
            value={timeframe}
            onChange={(event) => setTimeframe(event.target.value)}
          >
            <option value="1M">1M Historical</option>
            <option value="3M">3M Historical</option>
            <option value="6M">6M Historical</option>
            <option value="1Y">1Y Historical</option>
            <option value="3Y">3Y Historical</option>
            <option value="5Y">5Y Historical</option>
          </select>
        )}

        <button
          className="avatar"
          onClick={() => setPage('Profile')}
          title="Open profile"
        >
          A
        </button>
      </div>
    </header>
  );
}
