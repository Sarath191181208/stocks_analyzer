from .market import Market
from .stratergy import strategy
import pandas as pd


@strategy(
    name="Mean Reversion",
    description=""" Buy if stock is <90% of its moving average over `lookback` days. Sell if >110%. """,
)
def mean_reversion_strategy(
    portfolio, day, prices, market: Market, lookback=10, *args, **kwargs
):
    for stock, price in prices.items():
        avg = market.rolling_mean_on_day(stock, lookback, day)
        if avg is None or pd.isna(avg):
            continue

        if price < 0.9 * avg:  # undervalued → buy
            qty = int(portfolio.cash // (len(prices) * price))
            if qty > 0:
                portfolio.buy(stock, price, qty, day=day)

        elif price > 1.1 * avg:  # overvalued → sell
            qty = portfolio.holdings.get(stock, 0)
            if qty > 0:
                portfolio.sell(stock, price, qty, day=day)
