import pandas as pd
from typing import Tuple
import tqdm

from .market import Market
from .portfolio import Portfolio


def simulate_strategy(
    market: pd.DataFrame, strategy, initial_cash: float = 10000.0
) -> Tuple[pd.DataFrame, Portfolio]:
    """
    market: DataFrame with columns [name, day, price]
    strategy: function(portfolio: Portfolio, day: int, prices: dict) -> None
    """
    m = Market(market)
    return _simulate(m, strategy, initial_cash)

def _simulate(market: Market, strategy, initial_cash: float = 10_000.0) -> Tuple[pd.DataFrame, Portfolio]:
    portfolio = Portfolio(cash=initial_cash)
    results = []

    print(len(market.days))

    # Loop over days
    for day in tqdm.tqdm(market.days):
        prices_today = market.get_prices_on_day(day)

        # Strategy decides what to do
        strategy(portfolio, day, prices_today, market)

        # Record portfolio value
        results.append(
            {
                "day": day,
                "cash": portfolio.cash,
                "holdings_value": sum(
                    portfolio.holdings.get(s, 0) * p for s, p in prices_today.items()
                ),
                "total_value": portfolio.portfolio_value(prices_today),
            }
        )

    return pd.DataFrame(results), portfolio
