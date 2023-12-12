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
    historyIndex : int
    tradeHistory : list[list[tuple]]
    
    def __init__(self, controller, balance, botAlg) -> None:
        self.controller = controller
        self.capitalStart = balance
        self.capitalTotal = balance
        self.balance = balance
        self.profit = 0
        self.portfolio = []
        self.tradeHistory = []
        self.historyIndex = -1      
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
        
    def buyStock(self, s : Stock):
        self.addStock(s)
        self.updateBalance(-s.totalValue)
        self.updateHistory("Buy", s)
        
    def sellStock(self, i : int, amount : int = 1):
        stockChoice : Stock = self.popStock(i, amount)
        self.updateBalance(stockChoice.totalValue)
        self.updateHistory("Sell", stockChoice)
        
    def updateHistory(self, buySell, stock):
        # because stocks are updated every cycle, we have a reliable counter method
        block = (buySell, stock) # blocks should contain ("Buy"/"Sell", Stock object)
        self.tradeHistory[self.historyIndex] += [block]
    
    def getStocks(self):
        # returns a table-able list of stocks
        stocksData = []
        for stock in self.portfolio:
            stocksData.append([stock.name, stock.valueBought, stock.currentValue, stock.amount, stock.totalValue])
        return stocksData
    
    def updateStocks(self, data : list):
        self.historyIndex += 1 # increment for update history
        self.tradeHistory += [[]]
        
        dataLen = len(data)
        for i in range(dataLen):
            dataRow = data[i]
            currentStock = (dataRow[0], dataRow[-1])
            for j in range(len(self.portfolio)):
                playerStock : Stock = self.portfolio[j]
                if playerStock.name == currentStock[0]:
                    playerStock.update(currentStock[1])
    
    def getHistory(self) -> list:
        # returns a list that conforms to HistoryScreen, except for month
        historyList : list = []
        for i in range(len(self.tradeHistory)):
            month = self.tradeHistory[i]
            for block in month:
                stock : Stock = block[1]
                blockInfo : list = [i, block[0], stock.name, stock.currentValue, stock.amount, stock.totalValue]
                historyList.append(blockInfo)
        return historyList
    
    def determineProfits(self):
        # assume already updated
        stockSum : float = 0
        for stock in self.portfolio:
            stockSum += stock.totalValue
        self.capitalTotal = self.balance + stockSum
        self.profit = self.capitalTotal - self.capitalStart