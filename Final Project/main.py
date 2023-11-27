from trader import Trader
from bot import Stock
from bot import Bot


class GameManager:
    header = ["Stock", "M1", "M2"]
    data : list = []
    traders : list
    currentTime : int
    timeframeStart : int
    timeframeEnd : int
    currentScreen : int
    displays : dict = {"AllStocks": 1, "PlayerStocks" : 2}
    
    def sData(self, data): 
        # all of these sName functions are set functions
        self.data = data
        return self
    
    def sTraders(self, traders : list):
        self.traders = traders
        return self
    
    def sTimeframe(self, start, end):
        self.currentTime = start
        self.timeframeStart = start
        self.timeframeEnd = end
        return self
    
    def getData(self):
        data = [self.header]
        for d in self.data:
            data.append(d)
        return data
    
    def gameStart(self):
        gameRunning = True
        while gameRunning:
            gameRunning = self.currentTime <= self.timeframeEnd
            
            self.progress()
        self.endGame()
                
    def progress(self):
        if self.currentTime >= len(self.data):
            raise IndexError("Current time has surpassed size of data.")
        
        # TODO: Would be nice to rework this into a screenManager
        self.currentDisplay = self.displays["AllStocks"]
        tableData = self.getData()
        table = buildTable(tableData)
        displayTable(table)
        
        for t in self.traders:
            currTrader : Trader = t
            self.traderAction(t)
        self.currentTime = self.currentTime + 1
    
    def endGame(self):
        for t in self.traders:
            displayTraderInfo(t)

    def traderAction(self, trader : Trader):
        if (trader.getController() == "Player"):
            choosing = True
            while choosing:
                buySell : str = inputClean("Buy stock or sell stock? [b, s, n] ")
                buySell = buySell.lower()
                match buySell:
                    case "b":
                        self.buyStock(trader)
                    
                    case "s":
                        self.sellStock(trader)
                    
                    case "n":
                        choosing = False
                    
                    case _:
                        print("Please input either b or s for buy or sell respectively, or n to exit.")
        else:
            self.sellStock(trader)
            self.buyStock(trader)

    # it is frustrating how messy all of this is, but if it works I'll be happy
    def buyStock(self, trader : Trader):
        if (trader.getController() == "Player"):
            choosing = True
            while choosing:
                try:
                    choice = int(inputClean("Which stock to buy? ")) - 1
                    if choice == -1:
                        stockTup = None
                        choosing == False
                    else:
                        stockTup = (self.data[choice][0], self.data[choice][self.currentTime])
                        choosing = self.verifyChoice(stockTup)
                except:
                    print(f"Please input a whole number between 1 and {len(self.data)}, or 0 to choose none.")
        
        if stockTup != None:
            stockChoice : Stock = Stock(stockTup[0], stockTup[1])
            trader.addStock(stockChoice)

    # TODO: implement selling stocks
    def sellStock(self, trader : Trader):
        # need to get the current value of the stock
        if (trader.getController() == "Player"):
            playerStockCount = len(trader.stocks)
            choosing = playerStockCount != 0
            if not choosing:
                print("You have no stocks to sell!")
                return

            
            while choosing:
                try:
                    choice = int(inputClean("Which stock to sell? ")) - 1
                    if choice == -1:
                        stockTup = None
                        choosing == False
                    else:
                        stockChoice : Stock = trader.stocks[choice] 
                        stockTup = (stockChoice.name, stockChoice.value)
                        choosing = self.verifyChoice(stockTup, 1)
                except:
                    print(f"Please input a whole number between 1 and {len(trader.stocks)}, or 0 to choose none.")
        
        if stockTup != None:
            trader.popStock(stockChoice)

    def verifyChoice(self, choice, buySell = 0):
        # should take the choice after choose stock is called
        verifying = True
        bs = ("Buy", "Sell")
        while verifying:
            answer : str = inputClean(f"Are you sure you want to {bs[buySell]} {choice[0]} at {choice[1]}? [y/n] ")
            answer = answer.lower()
            if answer != 'y' and answer != 'n':
                print("Please input a valid answer [y/n].")
            else:
                return answer == 'n'


@staticmethod
def displayTable(table : list):
    # should only take an array of strings as input
    tableLength : int = len(table)
    for i in range(tableLength):
        print(table[i])
    
@staticmethod
def buildTable(data : list):
    # First row of data should be the header
    header = data[0]
    row = len(data)
    col = len(header)
    
    
    maxColArray = [] # holds the greatest length of an element found in each column
    for j in range(col): 
        maxColArray.append(len(header[j])) # initialize with the header elements
    for i in range(1, row):
        for j in range(col):
            elem = str(data[i][j])
            elemSize = len(elem)
            if elemSize > maxColArray[j]:
                maxColArray[j] = elemSize
    
    # assemble the header
    tableArray = []
    stringBuffer = ""
    vertLine = "  | " # this variable creates the separators
    for j in range(col):
        maxSize = maxColArray[j]
        stringBuffer += fillEmptySpace(header[j], maxSize)
        if j != (col - 1): # if i == last element
            stringBuffer += vertLine
    tableArray.append(stringBuffer)
    
    # add a line separating the header from the data
    stringBuffer = ""
    for j in range(col):
        stringBuffer += "-" * maxColArray[j]
        if j != (col - 1):
            stringBuffer += vertLine.replace(" ", "-")
        else:
            stringBuffer += "-"
    tableArray.append(stringBuffer)
    
    # build each row of the table
    for i in range(1, row):
        stringBuffer = ""
        for j in range(col):
            maxSize = maxColArray[j]
            elem = str(data[i][j])
            elem = fillEmptySpace(elem, maxSize)
            stringBuffer += elem
            if j != (col - 1):
                stringBuffer += vertLine
        tableArray.append(stringBuffer)
    
    return tableArray

@staticmethod
def fillEmptySpace(s : str, maxLength : int):
        inputLength = len(s)
        stringBuffer = s
        if inputLength > maxLength:
            raise ValueError("Max length of a column value is larger than expected")
        diff = maxLength - inputLength
        for i in range(diff):
            stringBuffer = stringBuffer + " "
            #alt = i % 2
            #match alt:
            #    case 0:
            #        stringBuffer = " " + stringBuffer
            #    case 1:
            #        stringBuffer = stringBuffer + " "
            
        return stringBuffer

@staticmethod
def displayTraderInfo(t : Trader):
    bufferString = f"{t.controller}:" + "\n" + f"Profit: {t.profit}"
    for s in t.stocks:
        bufferString = bufferString + "\n"
        bufferString = bufferString + s.name
    return bufferString

@staticmethod
def inputClean(s : str):
    result : str = ""
    try:
        result : str = input(s)
    except EOFError:
        exit()
    return result

def main():
    playerBal = 100
    testData = [["AMC", 4.5, 7],["GME", 555, 6],["BBBYQ", 8, 999]]
    player = Trader("Player", playerBal)
    traders = [player]
    gameManager = GameManager()
    gameManager.sData(testData).sTimeframe(1, 6).sTraders(traders)
    gameManager.gameStart()
    
    

main()