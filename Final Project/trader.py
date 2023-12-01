class Stock:
    name : str
    valueBought : float
    currentValue : float
    buyIndex : int
    amount : int
    totalValue : float
    
    def __init__(self, name : str, currentValue : float, buyIndex : int, amount : int = 1) -> None:
        self.name = name
        self.valueBought = currentValue
        self.currentValue = currentValue # could reference the index of the stock instead
        self.amount = amount
        self.buyIndex = buyIndex
        self.totalValue = self.currentValue * self.amount
    
    def update(self, newValue : float):
        self.currentValue = newValue
        self.totalValue = self.currentValue * self.amount
    
    def resetTotalValue(self):
        self.totalValue = self.currentValue * self.amount
        

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
    
    def popStock(self, i : int, amount : int = 1):
        stock : Stock = self.portfolio[i]
        diff = stock.amount - amount
        if diff < 0:
            raise ValueError("Subtracted too many stocks!")
        if diff == 0:
            stock = self.portfolio.pop(i)
        else:
            self.portfolio[i].amount = diff
            self.portfolio[i].resetTotalValue()
            stock.amount = amount
            stock.resetTotalValue()
        return stock
    
    def updateBalance(self, n : int):
        self.balance += n
        self.balance = round(self.balance, 2)
        if self.controller == "Player":
            print(f"New Balance: {self.balance}")
        
    def getStocks(self):
        # returns a table-able list of stocks
        stocksData = []
        for stock in self.portfolio:
            stocksData.append([stock.name, stock.valueBought, stock.currentValue, stock.amount, stock.totalValue])
        return stocksData
    
    def updateStocks(self, data : list):
        dataLen = len(data)
        for i in range(dataLen):
            dataRow = data[i]
            currentStock = (dataRow[0], dataRow[-1])
            for j in range(len(self.portfolio)):
                playerStock : Stock = self.portfolio[j]
                if playerStock.name == currentStock[0]:
                    playerStock.update(currentStock[1])
    
    def determineProfits(self):
        # assume already updated
        stockSum : float = 0
        for stock in self.portfolio:
            stockSum += stock.currentValue
        self.capitalTotal = self.balance + stockSum
        self.profit = self.capitalTotal - self.capitalStart