import pathlib
import sys
import unittest
from importlib import import_module


ROOT = pathlib.Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

monte_carlo = import_module("app.quant_engine.monte_carlo")
build_monte_carlo_payload = monte_carlo.build_monte_carlo_payload
simulate_gbm_paths = monte_carlo.simulate_gbm_paths
summarize_simulations = monte_carlo.summarize_simulations


class TestMonteCarlo(unittest.TestCase):
    def test_simulate_gbm_paths_shape_and_initial_value(self):
        paths = simulate_gbm_paths(
            last_price=100.0,
            mean_return=0.10,
            volatility=0.20,
            days=30,
            simulations=50,
            seed=123,
        )

        self.assertEqual(paths.shape, (31, 50))
        self.assertTrue((paths.iloc[0] == 100.0).all())

    def test_simulate_gbm_paths_invalid_inputs(self):
        with self.assertRaisesRegex(ValueError, "last_price must be positive"):
            simulate_gbm_paths(0, 0.1, 0.2)

        with self.assertRaisesRegex(ValueError, "days must be positive"):
            simulate_gbm_paths(100, 0.1, 0.2, days=0)

        with self.assertRaisesRegex(ValueError, "simulations must be positive"):
            simulate_gbm_paths(100, 0.1, 0.2, simulations=0)

    def test_summarize_simulations_returns_expected_fields(self):
        paths = simulate_gbm_paths(
            last_price=120.0,
            mean_return=0.05,
            volatility=0.15,
            days=10,
            simulations=8,
            seed=7,
        )
        summary = summarize_simulations(paths)

        expected_keys = {
            "expected_final_price",
            "median_final_price",
            "worst_case_5pct",
            "best_case_95pct",
            "min_final_price",
            "max_final_price",
            "simulations",
            "days",
        }

        self.assertEqual(set(summary.keys()), expected_keys)
        self.assertEqual(summary["simulations"], 8)
        self.assertEqual(summary["days"], 10)

    def test_build_monte_carlo_payload_sample_paths_shape(self):
        payload = build_monte_carlo_payload(
            last_price=95.0,
            mean_return=0.07,
            volatility=0.18,
            days=12,
            simulations=5,
        )

        self.assertIn("summary", payload)
        self.assertIn("sample_paths", payload)
        self.assertEqual(len(payload["sample_paths"]), 13)

        first_row = payload["sample_paths"][0]
        self.assertEqual(first_row["day"], 0)

        for idx in range(5):
            self.assertIn(f"path_{idx}", first_row)


if __name__ == "__main__":
    unittest.main()
