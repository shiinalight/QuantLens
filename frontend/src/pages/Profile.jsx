import Card from '../components/Card';

const strategyLeaderboard = [
  {
    name: 'Momentum Rotation',
    return: '18.4%',
    sharpe: '1.42',
    winRate: '63%',
  },
  {
    name: 'Mean Reversion',
    return: '11.2%',
    sharpe: '0.96',
    winRate: '58%',
  },
  {
    name: 'Volatility Targeting',
    return: '14.7%',
    sharpe: '1.31',
    winRate: '61%',
  },
  {
    name: 'Moving Average Crossover',
    return: '9.5%',
    sharpe: '0.81',
    winRate: '54%',
  },
];

const activities = [
  'Added CAPM factor model analytics',
  'Integrated historical VaR and CVaR',
  'Built optimizer API endpoint',
  'Implemented portfolio volatility engine',
  'Connected FastAPI analytics backend',
];

export default function Profile() {
  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">QuantLens Research Profile</p>

          <h1>Quantitative Research Workspace</h1>

          <p className="muted">
            Quant-focused portfolio analytics and strategy research environment.
          </p>
        </div>

        <div className="profile-avatar-large">
          A
        </div>
      </div>

      <div className="grid two">
        <Card title="Research Identity">
          <div className="summary">
            <div>
              <span>Role</span>
              <b>Quant Researcher</b>
            </div>

            <div>
              <span>Primary Focus</span>
              <b>Portfolio Optimization</b>
            </div>

            <div>
              <span>Asset Universe</span>
              <b>Equities / ETFs</b>
            </div>

            <div>
              <span>Preferred Benchmark</span>
              <b>SPY</b>
            </div>

            <div>
              <span>Factor Framework</span>
              <b>CAPM / Risk-Based</b>
            </div>

            <div>
              <span>Research Style</span>
              <b>Systematic Quantitative</b>
            </div>
          </div>
        </Card>

        <Card title="Quant Metrics Snapshot">
          <div className="summary">
            <div>
              <span>Sharpe Ratio</span>
              <b className="good">1.42</b>
            </div>

            <div>
              <span>Annual Volatility</span>
              <b>14.7%</b>
            </div>

            <div>
              <span>Portfolio Beta</span>
              <b>0.94</b>
            </div>

            <div>
              <span>Maximum Drawdown</span>
              <b className="bad">-11.2%</b>
            </div>

            <div>
              <span>Historical VaR</span>
              <b className="bad">-2.4%</b>
            </div>

            <div>
              <span>CAGR</span>
              <b className="good">16.1%</b>
            </div>
          </div>
        </Card>
      </div>

      <div className="grid two">
        <Card title="Strategy Performance">
          <div className="strategy-table">
            <div className="strategy-header">
              <span>Strategy</span>
              <span>Return</span>
              <span>Sharpe</span>
              <span>Win Rate</span>
            </div>

            {strategyLeaderboard.map((strategy) => (
              <div
                key={strategy.name}
                className="strategy-row"
              >
                <span>{strategy.name}</span>
                <span className="good">
                  {strategy.return}
                </span>
                <span>{strategy.sharpe}</span>
                <span>{strategy.winRate}</span>
              </div>
            ))}
          </div>
        </Card>

        <Card title="Research Domains">
          <div className="tag-cloud">
            <span>Portfolio Optimization</span>
            <span>Risk Modeling</span>
            <span>VaR / CVaR</span>
            <span>CAPM</span>
            <span>Backtesting</span>
            <span>Time Series</span>
            <span>Volatility Analysis</span>
            <span>Alpha Research</span>
            <span>Factor Investing</span>
            <span>Systematic Trading</span>
          </div>
        </Card>
      </div>

      <Card title="Research Activity Timeline">
        <div className="activity-list">
          {activities.map((activity) => (
            <div
              key={activity}
              className="activity-item"
            >
              <div className="activity-dot" />
              <span>{activity}</span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}