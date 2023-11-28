from bot import Stock

class Trader:
    controller : str
    balance : float
    stocks : list = []
    profit : float
    
    def __init__(self, controller, balance) -> None:
        self.controller = controller
        self.balance = balance
        self.profit = 0

    def getController(self):
        return self.controller
    
    def addStock(self, stock):
        self.stocks.append(stock)
    
    def popStock(self, i):
        return self.stocks.pop(i)
    
    def getStocks(self):
        # returns a table-able list of stocks
        stocksData = []
        for stock in self.stocks:
            stocksData.append([stock.name, stock.value])
        return stocksData