import React from 'react';
import Card from '../components/Card';
import { fmt } from '../utils/format';

export default function MarketView({ data }) {
  const heatmap = data?.heatmap || [];
  const volumeSpikes = data?.volume_spikes || [];

  return (
    <main className="page">
      <h1>Market View</h1>
      <p>Real market overview and volume scanners</p>

      <div className="grid two-one">
        <Card title="Market Map">
          <div className="heatmap">
            {heatmap.map((item) => (
              <div className={item.daily_return >= 0 ? 'green' : 'red'} key={item.ticker}>
                {item.ticker}
                <br />
                <small>{fmt(item.daily_return, '%')}</small>
              </div>
            ))}
          </div>
        </Card>

        <Card title="Volume Spikes">
          <table>
            <tbody>
              {volumeSpikes.map((item) => (
                <tr key={item.ticker}>
                  <td>{item.ticker}</td>
                  <td>{item.volume.toLocaleString()}</td>
                  <td className={item.volume_ratio >= 1 ? 'good' : 'bad'}>
                    {item.volume_ratio.toFixed(2)}x
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      </div>

      <div className="grid two">
        <Card title="Top Gainers">
          <MarketTable items={data?.top_gainers || []} valueKey="daily_return" suffix="%" />
        </Card>

        <Card title="Top Losers">
          <MarketTable items={data?.top_losers || []} valueKey="daily_return" suffix="%" />
        </Card>
      </div>

      <div className="grid two">
        <Card title="Rolling Volatility Scanner">
          <MarketTable items={data?.volatility_scanner || []} valueKey="rolling_volatility" suffix="%" />
        </Card>

        <Card title="Relative Strength 5D">
          <MarketTable items={data?.relative_strength || []} valueKey="five_day_return" suffix="%" />
        </Card>
      </div>
    </main>
  );
}

function MarketTable({ items, valueKey, suffix = '' }) {
  return (
    <table>
      <tbody>
        {items.map((item) => (
          <tr key={item.ticker}>
            <td>{item.ticker}</td>
            <td>${item.price}</td>
            <td className={item[valueKey] >= 0 ? 'good' : 'bad'}>
              {fmt(item[valueKey], suffix)}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
