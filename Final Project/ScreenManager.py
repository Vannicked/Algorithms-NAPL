
class Screen:
    name : str
    data : str
    
    def __init__(self, name) -> None:
        self.name = name
        self.data = "This is an empty screen."
    
    def display(self):
        print(self.data)

    def update(self, data):
        self.data = data

class TableScreen(Screen):
    header : list
    data : list
    
    def __init__(self, name) -> None:
        super().__init__(name)
        self.header = []
    
    def display(self):
        table = []
        if len(self.header) > 0: # in the event of a dynamic header vs a static one
            table = [self.header]
        table += self.data
        displayTable(table)

class EndScreen(TableScreen):
    header : list
        
    def __init__(self, name) -> None:
        super().__init__(name)
        self.header : list = ["Trader", "Starting Balance", "Ending Capital", "Profit"]


# screen doesn't look like a word anymore
class ScreenManager:
        
    screen : Screen
    possibleScreens : dict
    
    def __init__(self):
        playerStocks = TableScreen("TraderStocks")
        playerStocks.header = ["Stock", "Bought At", "Now At", "Quantity", "Total Value"] # this kind of meta programming feels bad
        
        screens : list[Screen] = [Screen("Empty"), TableScreen("StockTable"), playerStocks, EndScreen("EndScreen")]
        self.possibleScreens = {}
        
        
        for screen in screens:
            self.possibleScreens[screen.name] = screen
        
        self.screen = self.possibleScreens["Empty"]
    
    def screenChange(self, screenName):
        # sometimes we want a screen that changes, sometimes we don't
        if screenName != self.screen.name:
            self.screen : Screen = self.possibleScreens[screenName]
            self.screen.display()
    
    def request(self, screenName, data : list = None):
        if data != None:
            newScreen : Screen = self.possibleScreens[screenName]
            newScreen.update(data)
            self.possibleScreens[screenName] = newScreen
        
        self.screen : Screen = self.possibleScreens[screenName]
        self.screen.display()
    
    def update(self, screenName, data):
        screen : Screen = self.possibleScreens[screenName]
        screen.update(data)


@staticmethod
def displayTable(data : list):
    # requires a table that has a header appended to the front

    table = buildTable(data) # this creates a dependency, but that's okay, I hope
    
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
