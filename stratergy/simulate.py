import pandas as pd
from typing import Tuple
from .portfolio import Portfolio

def simulate_strategy(market: pd.DataFrame, strategy, initial_cash: float = 10000.0) -> Tuple[pd.DataFrame, Portfolio]:
    """
    market: DataFrame with columns [name, day, price]
    strategy: function(portfolio: Portfolio, day: int, prices: dict) -> None
    """
    portfolio = Portfolio(cash=initial_cash)
    results = []

    # Loop over days
    for day in sorted(market["day"].unique()):
        prices_today = (
            market[market["day"] == day]
            .set_index("name")["price"]
            .to_dict()
        )

        # Strategy decides what to do
        strategy(portfolio, day, prices_today)

        # Record portfolio value
        results.append({
            "day": day,
            "cash": portfolio.cash,
            "holdings_value": sum(portfolio.holdings.get(s,0)*p for s,p in prices_today.items()),
            "total_value": portfolio.portfolio_value(prices_today)
        })

    return pd.DataFrame(results), portfolio
