import numpy as np


def _curve(seed: int, n: int = 18, drift: float = 1.35):
    rng = np.random.default_rng(seed)
    vals = np.cumsum(rng.normal(drift, 4.5, n))
    vals = vals - vals.min() + rng.uniform(0, 3)

    labels = [
        "Jan 23", "Feb 23", "Mar 23", "Apr 23", "May 23", "Jun 23",
        "Jul 23", "Aug 23", "Sep 23", "Oct 23", "Nov 23", "Dec 23",
        "Jan 24", "Feb 24", "Mar 24", "Apr 24", "May 24", "Jun 24",
        "Jul 24", "Aug 24", "Sep 24", "Oct 24", "Nov 24", "Dec 24",
    ]

    return [{"date": labels[i], "value": round(float(vals[i]), 2)} for i in range(n)]


def build_demo_payload():
    rng = np.random.default_rng(7)

    monthly = [
        {"month": m, "return": round(float(rng.normal(3, 5)), 2)}
        for m in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ]

    drawdown = [
        {"date": x["date"], "dd": round(-abs(float(rng.normal(5, 4))), 2)}
        for x in _curve(3)
    ]

    signal = [
        {"date": x["date"], "signal": round(float(rng.normal(0, 0.75)), 2)}
        for x in _curve(5, 24)
    ]

    names = [
        ("Momentum 20/50", "Momentum", 28.41, 1.47, -7.21, 35.2, 1),
        ("Mean Reversion", "Reversal", 17.32, 1.12, -6.18, 28.7, 2),
        ("VWAP Deviation", "Intraday", 11.09, 0.85, -4.32, 22.4, 3),
    ]

    strategies = [
        {
            "name": n,
            "category": c,
            "return": r,
            "sharpe": s,
            "drawdown": d,
            "turnover": t,
            "curve": _curve(seed),
        }
        for n, c, r, s, d, t, seed in names
    ]

    return {
        "equity": _curve(42, 18, 1.6),
        "monthly": monthly,
        "drawdown": drawdown,
        "signal": signal,
        "strategies": strategies,
    }