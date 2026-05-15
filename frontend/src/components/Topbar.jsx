import React from 'react';

export default function Topbar({ ticker, setTicker, page }) {
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

        {showTicker && <button>1Y Historical</button>}

        <button className="avatar">A</button>
      </div>
    </header>
  );
}
