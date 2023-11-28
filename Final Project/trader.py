class Stock:
    name : str
    valueBought : int
    currentValue : int
    
    def __init__(self, name, value) -> None:
        self.name = name
        self.valueBought = value
        self.currentValue = value


class Trader:
    controller : str
    balance : float
    portfolio : list
    profit : float
    
    def __init__(self, controller, balance) -> None:
        self.controller = controller
        self.balance = balance
        self.profit = 0
        self.portfolio = []

    def getController(self):
        return self.controller
    
    def addStock(self, stock):
        self.portfolio.append(stock)
    
    def popStock(self, i : int):
        return self.portfolio.pop(i)
    
    def getStocks(self):
        # returns a table-able list of stocks
        stocksData = []
        for stock in self.portfolio:
            stocksData.append([stock.name, stock.valueBought, stock.currentValue])
        return stocksData
    
    def updateStocks(self, data : list):
        dataLen = len(data)
        for i in range(dataLen):
            dataRow = data[i]
            currentStock = (dataRow[0], dataRow[-1])
            for j in range(len(self.portfolio)):
                playerStock : Stock = self.portfolio[j]
                if playerStock.name == currentStock[0]:
                    playerStock.currentValue = currentStock[1]