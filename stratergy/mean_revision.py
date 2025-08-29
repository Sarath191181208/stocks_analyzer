from .market import Market
from .stratergy import strategy


@strategy(
    name="Mean Revision",
    description=""" Buy if stock is <90% of its moving average over `lookback` days. Sell if >110%. """,
)
def mean_reversion_strategy(
    portfolio, day, prices, market: Market, lookback=10, *args, **kwargs
):
    """
    Buy if stock is <90% of its moving average over `lookback` days.
    Sell if >110%.
    """

    for stock, price in prices.items():
        series = market.get_prices_for_stock(stock)
        past_days = series.loc[:day].tail(lookback)

        if len(past_days) < lookback:
            continue  # not enough history

        avg = past_days.mean()

        if price < 0.9 * avg:  # undervalued
            qty = int(portfolio.cash // (len(prices) * price))
            if qty > 0:
                portfolio.buy(stock, price, qty, day=day)

        elif price > 1.1 * avg:  # overvalued
            qty = portfolio.holdings.get(stock, 0)
            if qty > 0:
                portfolio.sell(stock, price, qty, day=day)
