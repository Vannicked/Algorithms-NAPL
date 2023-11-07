from trader import Trader
import bot


class GameManager:
    header = ["Stock", "M1", "M2"]
    data : list = []
    traders : list
    currentTime : int
    timeframeStart : int
    timeframeEnd : int
    
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
        
        tableData = self.getData()
        table = buildTable(tableData)
        displayTable(table)
        
        for t in self.traders:
            currTrader : Trader = t
            self.buyStock(currTrader)
        self.currentTime = self.currentTime + 1
    
    def endGame(self):
        for t in self.traders:
            displayTraderInfo(t)

    def buyStock(self, trader : Trader):
        if (trader.getController() == "Player"):
            choosing = True
            while choosing:
                try:
                    choice = int(input("Which stock to invest? ")) - 1
                    if choice == -1:
                        stockTup = None
                        choosing == False
                    else:
                        stockTup = (self.data[choice][0], self.data[choice][self.currentTime])
                        choosing = self.verifyChoice(stockTup)
                except:
                    print(f"Please input a whole number between 1 and {len(self.data)}, or 0 to choose none.")
        
        if stockTup != None:
            stockChoice : bot.Stock = bot.Stock(stockTup[0], stockTup[1])
            trader.addStock(stockChoice)

    # TODO: implement selling stocks

    def verifyChoice(self, choice):
        # should take the choice after choose stock is called
        verifying = True
        while verifying:
            answer : str = input(f"Are you sure you want to buy {choice[0]} at {choice[1]}? [y/n] ")
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

def main():
    playerBal = 100
    testData = [["AMC", 4.5, 7],["GME", 555, 6],["BBBYQ", 8, 999]]
    player = Trader("Player", playerBal)
    traders = [player]
    gameManager = GameManager()
    gameManager.sData(testData).sTimeframe(1, 6).sTraders(traders)
    gameManager.gameStart()
    
    

main()