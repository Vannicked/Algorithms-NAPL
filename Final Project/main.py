from trader import Trader

class GameManager:
    header = ["Stock", "M1", "M2"]
    data : list = []
    traders : list
    currentTime : int
    timeframeStart : int
    timeframeEnd : int
    
    def sData(self, data):
        self.data = data
        return self
    
    def sTraders(self, traders : list):
        self.traders = traders
        return self
    
    def sTimeframe(self, start, end):
        self.timeframeStart = start
        self.timeframeEnd = end
        return self
    
    def getData(self):
        data = [self.header]
        for d in self.data:
            data.append(d)
        return data
    
    def progress(self):
        if currentTime == self.timeframeEnd:
            self.endGame()
        else:
            currentTime = currentTime + 1
    
    def endGame(self):
        for t in self.traders:
            displayTraderInfo(t)

    def chooseStock(self, trader):
        if (trader.getController == "Player"):
            choice = input("Which stock to invest? ")
            try:
                choice = int(choice)
                return choice
            except:
                print(f"Please input a whole number between 1 and {self.data.length}")

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
    game = GameManager()
    game.sData(testData).sTimeframe(1, 6).sTraders(traders)
    tableData = game.getData()
    table = buildTable(tableData)
    displayTable(table)
    
    

main()