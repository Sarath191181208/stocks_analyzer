class Portfolio:
    def __init__(self, cash: float = 10000.0):
        self.cash = cash
        self.holdings = {}  # stock -> shares
        self.history = []

    def buy(self, stock: str, price: float, qty: int, day: int):
        cost = price * qty
        if self.cash >= cost:
            self.cash -= cost
            self.holdings[stock] = self.holdings.get(stock, 0) + qty
            self.history.append((day, "BUY", stock, qty, price, self.cash))
    
    def sell(self, stock: str, price: float, qty: int, day: int):
        if self.holdings.get(stock, 0) >= qty:
            self.holdings[stock] -= qty
            self.cash += price * qty
            self.history.append((day, "SELL", stock, qty, price, self.cash))

    def portfolio_value(self, prices: dict):
        value = self.cash
        for stock, qty in self.holdings.items():
            if stock in prices:
                value += qty * prices[stock]
        return value
