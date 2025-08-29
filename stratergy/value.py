from .market import Market
from .stratergy import strategy


@strategy(
    name="Value",
    description=""" 
    Always invest in the `top_n` cheapest stocks.
    """,
)
def value_strategy(portfolio, day, prices, market: Market, top_n=3, *args, **kwargs):
    """
    Always invest in the `top_n` cheapest stocks.
    """

    cheapest = sorted(prices.items(), key=lambda x: x[1])[:top_n]
    cheapest_set = {stock for stock, _ in cheapest}

    # Buy cheapest
    for stock, price in cheapest:
        if portfolio.holdings.get(stock, 0) == 0:
            qty = int(portfolio.cash // (top_n * price))
            if qty > 0:
                portfolio.buy(stock, price, qty, day=day)

    # Sell those that are no longer cheapest
    for stock, qty in list(portfolio.holdings.items()):
        if qty > 0 and stock not in cheapest_set:
            portfolio.sell(stock, prices[stock], qty, day=day)
