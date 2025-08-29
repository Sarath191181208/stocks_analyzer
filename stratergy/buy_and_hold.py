from .stratergy import strategy
from .market import Market


@strategy(
    name="Buy And Hold", description="Buys the minium stock and holds it till last day"
)
def buy_and_hold(portfolio, day, prices, market: Market, *args, **kwargs):
    if not day == 0:
        return
    cheapest = min(prices, key=prices.get)
    portfolio.buy(cheapest, prices[cheapest], qty=10, day=day)
