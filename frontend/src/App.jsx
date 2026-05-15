import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { BarChart3, Brain, FlaskConical, Home, LineChart, Newspaper, Settings, Wallet } from 'lucide-react';
import Card from './components/Card';
import Topbar from './components/Topbar';
import Dashboard from './pages/Dashboard';
import StrategyExplorer from './pages/StrategyExplorer';
import AlphaLab from './pages/AlphaLab';
import MarketView from './pages/MarketView';
import Backtests from './pages/Backtests';
import Portfolio from './pages/Portfolio';
import NewsSentiment from './pages/NewsSentiment';
import SettingsPage from './pages/SettingsPage';
import {
  getDemo,
  getMarket,
  getMarketOverview,
  getOptimizedPortfolio,
  getStrategy,
} from './services/api';
import './styles.css';

const nav = [
  ['Dashboard', Home], ['Strategy Explorer', FlaskConical], ['Alpha Lab', Brain], ['Market View', BarChart3], ['Portfolio', Wallet], ['Backtests', LineChart], ['News & Sentiment', Newspaper], ['Settings', Settings]
];

function Sidebar({ page, setPage }) {
  return <aside className="sidebar">
    <div className="brand"><div className="logo">◇</div><strong>QuantLens</strong></div>
    <nav>{nav.map(([n, Icon]) => <button key={n} onClick={() => setPage(n)} className={page === n ? 'active' : ''}><Icon size={16}/>{n}</button>)}</nav>
  </aside>
}

function Placeholder({ page }) { return <main className="page"><h1>{page}</h1><p>This page is scaffolded for the next milestone.</p><Card title="Coming next"><p>We can add portfolio optimization, risk parity, factor exposure, CAPM/Fama-French analysis, and AI strategy explanations here.</p></Card></main> }

function App(){
  const [page,setPage]=useState('Dashboard');
  const [ticker, setTicker] = useState("SPY");
  const [data,setData]=useState({equity:[],monthly:[],drawdown:[],signal:[],strategies:[]});
  const [marketOverview, setMarketOverview] = useState({ heatmap: [], volume_spikes: [] });
  const [portfolioData, setPortfolioData] = useState(null);
  const [portfolioMethod, setPortfolioMethod] = useState('equal_weight');
  const [strategyParams, setStrategyParams] = useState({
    shortWindow: 20,
    longWindow: 50,
    transactionCost: 0.001,
  });

  useEffect(() => {
    Promise.all([
      getDemo(),
      getMarket(ticker),
      getStrategy(
        'ma-crossover',
        `${ticker}?short_window=${strategyParams.shortWindow}&long_window=${strategyParams.longWindow}&transaction_cost=${strategyParams.transactionCost}`
      ),
      getStrategy('mean-reversion', ticker),
      getStrategy('momentum', ticker),
      getStrategy('volatility-breakout', ticker),
    ])
      .then(([demoData, marketData, maStrategy, mrStrategy, momentumStrategy, volStrategy]) => {
        setData({
          ...demoData,
          equity: marketData.equity,
          drawdown: marketData.drawdown,
          monthly: marketData.monthly,
          market: marketData,
          liveStrategy: maStrategy,
          strategies: [
            {
              name: maStrategy.name,
              category: 'Trend Following',
              return: maStrategy.total_return,
              alpha: maStrategy.excess_return,
              sharpe: maStrategy.sharpe_ratio,
              sortino: maStrategy.sortino_ratio,
              calmar: maStrategy.calmar_ratio,
              infoRatio: maStrategy.information_ratio,
              trackingError: maStrategy.tracking_error,
              beta: maStrategy.beta,
              var95: maStrategy.var_95,
              cvar95: maStrategy.cvar_95,
              drawdown: maStrategy.max_drawdown,
              turnover: maStrategy.turnover,
              curve: maStrategy.equity,
              benchmark: maStrategy.benchmark,
            },
            {
              name: mrStrategy.name,
              category: 'Mean Reversion',
              return: mrStrategy.total_return,
              alpha: mrStrategy.excess_return,
              sharpe: mrStrategy.sharpe_ratio,
              sortino: mrStrategy.sortino_ratio,
              calmar: mrStrategy.calmar_ratio,
              infoRatio: mrStrategy.information_ratio,
              trackingError: mrStrategy.tracking_error,
              beta: mrStrategy.beta,
              var95: mrStrategy.var_95,
              cvar95: mrStrategy.cvar_95,
              drawdown: mrStrategy.max_drawdown,
              turnover: mrStrategy.turnover,
              curve: mrStrategy.equity,
              benchmark: mrStrategy.benchmark,
            },
            {
              name: momentumStrategy.name,
              category: 'Momentum',
              return: momentumStrategy.total_return,
              alpha: momentumStrategy.excess_return,
              sharpe: momentumStrategy.sharpe_ratio,
              sortino: momentumStrategy.sortino_ratio,
              calmar: momentumStrategy.calmar_ratio,
              infoRatio: momentumStrategy.information_ratio,
              trackingError: momentumStrategy.tracking_error,
              beta: momentumStrategy.beta,
              var95: momentumStrategy.var_95,
              cvar95: momentumStrategy.cvar_95,
              drawdown: momentumStrategy.max_drawdown,
              turnover: momentumStrategy.turnover,
              curve: momentumStrategy.equity,
              benchmark: momentumStrategy.benchmark,
            },
            {
              name: volStrategy.name,
              category: 'Volatility',
              return: volStrategy.total_return,
              alpha: volStrategy.excess_return,
              sharpe: volStrategy.sharpe_ratio,
              sortino: volStrategy.sortino_ratio,
              calmar: volStrategy.calmar_ratio,
              infoRatio: volStrategy.information_ratio,
              trackingError: volStrategy.tracking_error,
              beta: volStrategy.beta,
              var95: volStrategy.var_95,
              cvar95: volStrategy.cvar_95,
              drawdown: volStrategy.max_drawdown,
              turnover: volStrategy.turnover,
              curve: volStrategy.equity,
              benchmark: volStrategy.benchmark,
            },
          ],
        });
      })
      .catch((error) => console.error('Failed to fetch data:', error));

    getMarketOverview()
      .then(setMarketOverview)
      .catch((error) => console.error('Failed to fetch market overview:', error));

    getOptimizedPortfolio(portfolioMethod)
      .then(setPortfolioData)
      .catch((error) => console.error('Failed to fetch portfolio:', error));
  }, [ticker, portfolioMethod, strategyParams]);

  const strategies=data.strategies||[];

  return (
    <div className="app">
      <Sidebar page={page} setPage={setPage}/>
      <div className="content">
        <Topbar ticker={ticker} setTicker={setTicker} page={page}/>
        {page==='Dashboard'&&<Dashboard data={data}/>} 
        {page==='Strategy Explorer'&&<StrategyExplorer strategies={strategies} strategyParams={strategyParams} setStrategyParams={setStrategyParams}/>} 
        {page==='Alpha Lab'&&<AlphaLab data={data}/>} 
        {page==='Market View'&&<MarketView data={marketOverview}/>} 
        {page==='Backtests'&&<Backtests strategies={strategies}/>}
        {page==='Portfolio'&&<Portfolio portfolio={portfolioData} method={portfolioMethod} setMethod={setPortfolioMethod}/>} 
        {page==='News & Sentiment'&&<NewsSentiment marketOverview={marketOverview}/>}
        {page==='Settings'&&<SettingsPage ticker={ticker}/>} 
        {!['Dashboard','Strategy Explorer','Alpha Lab','Market View','Backtests','Portfolio','News & Sentiment','Settings'].includes(page)&&<Placeholder page={page}/>} 
      </div>
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App/>);
