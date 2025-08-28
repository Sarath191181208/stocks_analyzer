def buy_and_hold(portfolio, day, prices):
    if day == 0:
        cheapest = min(prices, key=prices.get)
        portfolio.buy(cheapest, prices[cheapest], qty=10, day=day)
    elif day == max(prices):  # placeholder, sell all on last day
        for stock, price in prices.items():
            qty = portfolio.holdings.get(stock, 0)
            if qty > 0:
                portfolio.sell(stock, price, qty, day=day)
