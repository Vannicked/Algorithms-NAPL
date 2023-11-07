class Trader:
    controller : str
    balance : float
    stocks : list = []
    profit : float
    
    def __init__(self, controller, balance) -> None:
        self.controller = controller
        self.balance = balance
        self.profit = 100

    def getController(self):
        return self.controller
    
    def addStock(self, stock):
        self.stocks.append(stock)