from .market import Market
from .stratergy import strategy


@strategy(
    name="Momentum",
    description=""" 
    Buy if stock is up >5% compared to `lookback` days ago.
    Sell if down >5%.
    """,
)
def momentum_strategy(
    portfolio, day, prices, market: Market, lookback=5, *args, **kwargs
):
    """
    Buy if stock is up >5% compared to `lookback` days ago.
    Sell if down >5%.
    """

    for stock, price in prices.items():
        series = market.get_prices_for_stock(stock)
        if day - lookback not in series.index:
            continue  # not enough history

        past_price = series.loc[day - lookback]

        if price > past_price * 1.05:  # uptrend
            qty = int(portfolio.cash // (len(prices) * price))
            if qty > 0:
                portfolio.buy(stock, price, qty, day=day)

        elif price < past_price * 0.95:  # downtrend
            qty = portfolio.holdings.get(stock, 0)
            if qty > 0:
                portfolio.sell(stock, price, qty, day=day)
