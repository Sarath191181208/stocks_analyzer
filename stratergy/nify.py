from .market import Market
from .stratergy import strategy


@strategy(
    name="Nify",
    description=""" 
    Mimics an index-tracking strategy:
    - Every `rebalance_freq` days, select top N stocks by price.
    - Invest equally in them.
    - Hold until next rebalance.
    """,
)
def nifty_index_strategy(portfolio, day, prices, market: Market, top_n=5, rebalance_freq=30, *args, **kwargs):
    """
    Mimics an index-tracking strategy:
    - On day `rebalance_freq` days, select top N stocks by price.
    - Invest equally in them.
    - Hold until next rebalance.
    """

    if not (day % rebalance_freq == 0):
        return

    # rebalance 
    # Sell all current holdings before rebalancing
    for stock, qty in list(portfolio.holdings.items()):
        if qty > 0:
            portfolio.sell(stock, prices[stock], qty, day=day)

    # Pick top N by price (proxy for index components)
    top_stocks = sorted(prices.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Equal allocation across top N
    cash_per_stock = portfolio.cash / top_n if top_n > 0 else 0
    for stock, price in top_stocks:
        qty = int(cash_per_stock // price)
        if qty > 0:
            portfolio.buy(stock, price, qty, day=day)
