import numpy as np
import pandas as pd

from app.quant_engine.portfolio_optimization import (
    optimize_max_sharpe,
)


def build_demo_optimizer():
    """
    Demo expected returns and covariance matrix.
    """

    assets = ["SPY", "QQQ", "IWM", "TLT"]

    expected_returns = pd.Series(
        [0.12, 0.15, 0.10, 0.05],
        index=assets,
    )

    covariance_matrix = pd.DataFrame(
        [
            [0.040, 0.028, 0.025, 0.010],
            [0.028, 0.050, 0.030, 0.008],
            [0.025, 0.030, 0.060, 0.012],
            [0.010, 0.008, 0.012, 0.020],
        ],
        index=assets,
        columns=assets,
    )

    return optimize_max_sharpe(
        expected_returns,
        covariance_matrix,
    )