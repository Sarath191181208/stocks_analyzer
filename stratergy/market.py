from functools import cache
import pandas as pd


class Market:
    def __init__(self, data: pd.DataFrame):
        self.data = data

        # Precompute unique days
        self._days = sorted(self.data["day"].unique())

        # Pre-index prices by day (fast lookup)
        self._day_to_prices: dict[int, dict[str, float]] = {
            day: row.set_index("name")["price"].to_dict()
            for day, row in self.data.groupby("day")
        }

        # Pre-index prices by stock (fast lookup)
        self._stock_to_prices: dict[str, pd.Series] = {
            stock: row.set_index("day")["price"]
            for stock, row in self.data.groupby("name")
        }

    @property
    def days(self):
        return self._days

    def get_prices_on_day(self, day: int) -> dict[str, float]:
        return self._day_to_prices[day]

    @cache
    def get_prices_for_stock(self, stock: str) -> pd.Series:
        if stock not in self._stock_to_prices:
            raise ValueError(f"Stock {stock} not found in market data.")
        return self._stock_to_prices[stock]

    @cache
    def rolling_mean(self, stock: str, lookback: int) -> pd.Series:
        """Precompute + cache rolling mean for a stock/lookback."""
        series = self.get_prices_for_stock(stock)
        return series.rolling(lookback, min_periods=lookback).mean()

    def rolling_mean_on_day(self, stock: str, lookback: int, day: int) -> float | None:
        """Return rolling mean for stock at a given day."""
        return self.rolling_mean(stock, lookback).get(day, None)
