from functools import cache
import pandas as pd 

class Market:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    @property
    def days(self):
        return sorted(self.data["day"].unique())

    def get_prices_on_day(self, day: int) -> dict[str, float]:
        day_data = self.data[self.data["day"] == day]
        return day_data.set_index("name")["price"].to_dict()

    @cache
    def get_prices_for_stock(self, stock: str) -> pd.Series:
        d = self.data[self.data["name"] == stock].set_index("day")["price"]
        if d.empty:
            raise ValueError(f"Stock {stock} not found in market data.")
        return d
