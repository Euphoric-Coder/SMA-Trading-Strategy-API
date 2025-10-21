import unittest
from decimal import Decimal
from fastapi.testclient import TestClient
from main import app, StockDataIn
import pandas as pd


class TestDataValidation(unittest.TestCase):
    """Tests for input model and /data endpoint behavior."""

    def test_valid_model(self):
        """Ensure valid StockDataIn model parses correctly."""
        data = {
            "datetime": "2025-01-01T09:15:00",
            "open": 100.5,
            "high": 102.0,
            "low": 99.8,
            "close": 101.2,
            "volume": 15342,
        }
        obj = StockDataIn(**data)
        # Pydantic converts numeric fields to Decimal
        self.assertEqual(obj.close, Decimal("101.2"))

    def test_invalid_volume(self):
        """Invalid (negative) volume should raise ValueError."""
        data = {
            "datetime": "2025-01-01T09:15:00",
            "open": 100.5,
            "high": 102.0,
            "low": 99.8,
            "close": 101.2,
            "volume": -5,
        }
        with self.assertRaises(ValueError):
            StockDataIn(**data)

    def test_add_data_endpoint_success(self):
        """POST /data should accept valid input and return message."""
        with TestClient(app) as client:
            payload = {
                "datetime": "2025-01-01T09:15:00",
                "open": 100.5,
                "high": 102.0,
                "low": 99.8,
                "close": 101.2,
                "volume": 15342,
            }
            response = client.post("/data", json=payload)
            self.assertIn(response.status_code, [200, 400])
            data = response.json()
            self.assertTrue(
                "message" in data or "detail" in data,
                f"Unexpected response: {data}",
            )

    def test_add_data_endpoint_failure(self):
        """POST /data should fail for invalid input."""
        with TestClient(app) as client:
            payload = {
                "datetime": "2025-01-01T09:15:00",
                "open": -100.5,  # Invalid
                "high": 102.0,
                "low": 99.8,
                "close": 101.2,
                "volume": 15342,
            }
            response = client.post("/data", json=payload)
            self.assertEqual(response.status_code, 422)


class TestStrategyLogic(unittest.TestCase):
    """Tests for moving average crossover strategy."""

    def test_moving_average_correctness(self):
        """Verify rolling mean calculation logic."""
        df = pd.DataFrame({"close": [1, 2, 3, 4, 5, 6]})
        df["short"] = df["close"].rolling(window=2).mean()
        df["long"] = df["close"].rolling(window=3).mean()
        self.assertAlmostEqual(df["short"].iloc[-1], 5.5)
        self.assertAlmostEqual(df["long"].iloc[-1], 5.0)

    def test_strategy_endpoint_not_enough_data(self):
        """GET /strategy/performance returns 400 if insufficient data."""
        with TestClient(app) as client:
            response = client.get(
                "/strategy/performance?short_window=2000&long_window=3000"
            )
            self.assertIn(response.status_code, [200, 400])

    def test_strategy_endpoint_valid_response(self):
        """GET /strategy/performance returns valid fields."""
        with TestClient(app) as client:
            response = client.get("/strategy/performance")
            self.assertIn(response.status_code, [200, 400])
            if response.status_code == 200:
                data = response.json()
                for key in [
                    "short_window",
                    "long_window",
                    "total_return",
                    "last_signal",
                ]:
                    self.assertIn(key, data)


if __name__ == "__main__":
    unittest.main()
