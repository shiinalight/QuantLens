export const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

async function fetchJson(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export function getDemo() {
  return fetchJson('/api/demo');
}

export function getMarket(ticker) {
  return fetchJson(`/api/market/${ticker}`);
}

export function getStrategy(strategyName, ticker) {
  return fetchJson(`/api/strategy/${strategyName}/${ticker}`);
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
  return fetchJson('/api/alpha/run', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}
