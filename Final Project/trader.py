class Stock:
    name : str
    valueBought : float
    currentValue : float
    buyIndex : int
    
    def __init__(self, name : str, currentValue : float, buyIndex : int) -> None:
        self.name = name
        self.valueBought = currentValue
        self.currentValue = currentValue # could reference the index of the stock instead
        self.buyIndex = buyIndex

class Trader:
    controller : str
    capitalStart : float
    capitalTotal : float
    balance : float
    portfolio : list[Stock]
    profit : float
    botAlgorithm : int
    
    def __init__(self, controller, balance, botAlg) -> None:
        self.controller = controller
        self.capitalStart = balance
        self.capitalTotal = balance
        self.balance = balance
        self.profit = 0
        self.portfolio = []
        self.botAlgorithm = botAlg

    def getController(self):
        return self.controller
    
    def addStock(self, stock : Stock):
        self.portfolio.append(stock)
    
    def popStock(self, i : int):
        stock : Stock = self.portfolio.pop(i)
        return stock
    
    def updateBalance(self, n : int):
        self.balance += n
        
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
    
    def determineProfits(self):
        # assume already updated
        stockSum : float = 0
        for stock in self.portfolio:
            stockSum += stock.currentValue
        self.capitalTotal = self.balance + stockSum
        self.profit = self.capitalTotal - self.capitalStart