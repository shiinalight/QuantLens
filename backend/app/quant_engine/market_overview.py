import pandas as pd
import yfinance as yf


WATCHLIST = ["AAPL", "MSFT", "AMZN", "TSLA", "NVDA", "JPM", "BAC", "LLY", "JNJ", "CAT", "GE", "AMD"]


def build_market_overview():
    results = []

    for ticker in WATCHLIST:
        data = yf.download(ticker, period="5d", auto_adjust=True, progress=False)

        if data.empty or len(data) < 2:
            continue

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        close_today = float(data["Close"].iloc[-1])
        close_prev = float(data["Close"].iloc[-2])
        volume_today = int(data["Volume"].iloc[-1])
        avg_volume = float(data["Volume"].tail(5).mean())

        daily_return = ((close_today / close_prev) - 1) * 100
        five_day_return = ((close_today / float(data["Close"].iloc[-5])) - 1) * 100
        rolling_volatility = data["Close"].pct_change().tail(5).std() * (252 ** 0.5) * 100
        volume_ratio = volume_today / avg_volume if avg_volume else 0

        results.append({
            "ticker": ticker,
            "price": round(close_today, 2),
            "daily_return": round(daily_return, 2),
            "five_day_return": round(five_day_return, 2),
            "rolling_volatility": round(rolling_volatility, 2),
            "volume": volume_today,
            "volume_ratio": round(volume_ratio, 2),
        })

    return {
        "heatmap": results,
        "volume_spikes": sorted(results, key=lambda x: x["volume_ratio"], reverse=True)[:5],
        "top_gainers": sorted(results, key=lambda x: x["daily_return"], reverse=True)[:5],
        "top_losers": sorted(results, key=lambda x: x["daily_return"])[:5],
        "volatility_scanner": sorted(results, key=lambda x: x["rolling_volatility"], reverse=True)[:5],
        "relative_strength": sorted(results, key=lambda x: x["five_day_return"], reverse=True)[:5],
    }