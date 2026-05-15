const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

async function fetchJson(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

export function getDemo() {
  return fetchJson('/api/demo');
}

export function getMarket(ticker, timeframe = '1Y') {
  return fetchJson(`/api/market/${ticker}?timeframe=${encodeURIComponent(timeframe)}`);
}

export function getStrategy(strategyName, ticker, timeframe = '1Y') {
  const separator = ticker.includes('?') ? '&' : '?';
  return fetchJson(
    `/api/strategy/${strategyName}/${ticker}${separator}timeframe=${encodeURIComponent(timeframe)}`
  );
}

export function getMarketOverview() {
  return fetchJson('/api/market-overview');
}

export function getPortfolioEqualWeight() {
  return fetchJson('/api/portfolio/equal-weight');
}

export function getOptimizedPortfolio(method) {
  return fetchJson(`/api/portfolio/${method}`);
}

export async function runAlpha(payload) {
  const response = await fetch(`${API_BASE_URL}/api/alpha/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

export function getQuantAnalytics(ticker, timeframe = '1Y') {
  return fetchJson(`/api/analytics/${ticker}?timeframe=${encodeURIComponent(timeframe)}`);
}

export function getPortfolioOptimizer() {
  return fetchJson('/api/portfolio/optimizer');
}