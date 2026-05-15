import React from 'react';
import Card from '../components/Card';
import { fmt } from '../utils/format';

export default function NewsSentiment({ marketOverview }) {
  const movers = [...(marketOverview?.heatmap || [])]
    .sort((a, b) => Math.abs(b.daily_return) - Math.abs(a.daily_return))
    .slice(0, 6);

  return (
    <main className="page">
      <h1>News & Sentiment</h1>
      <p>Market movement proxy using real daily returns and volume activity</p>

      <div className="grid two">
        <Card title="Largest Daily Movers">
          <table>
            <tbody>
              {movers.map((item) => (
                <tr key={item.ticker}>
                  <td>{item.ticker}</td>
                  <td className={item.daily_return >= 0 ? 'good' : 'bad'}>
                    {fmt(item.daily_return, '%')}
                  </td>
                  <td>{item.price}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>

        <Card title="Sentiment Proxy">
          <div className="summary">
            {(marketOverview?.heatmap || []).map((item) => (
              <div key={item.ticker}>
                <span>{item.ticker}</span>
                <b className={item.daily_return >= 0 ? 'good' : 'bad'}>
                  {item.daily_return >= 0 ? 'Bullish' : 'Bearish'}
                </b>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </main>
  );
}
