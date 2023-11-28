class Stock:
    name : str
    valueBought : float
    currentValue : float
    
    def __init__(self, name : str, value : float) -> None:
        self.name = name
        self.valueBought = value
        self.currentValue = value


class Trader:
    controller : str
    starting_capital : float
    overall_capital : float
    balance : float
    portfolio : list[Stock]
    profit : float
    
    def __init__(self, controller, balance) -> None:
        self.controller = controller
        self.starting_capital = balance
        self.overall_capital = balance
        self.balance = balance
        self.profit = 0
        self.portfolio = []

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
        self.overall_capital = self.balance + stockSum
        self.profit = self.overall_capital - self.starting_capital