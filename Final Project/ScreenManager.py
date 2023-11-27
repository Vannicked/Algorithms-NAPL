
class Screen:
    name : str
    data : list
    
    def __init__(self, name) -> None:
        self.name = name
        self.data = []
    
    def display(self):
        print(self.data)

    def update(self, data):
        self.data = data

class TableScreen(Screen):
    
    def display(self):
        displayTable(self.data)



# screen doesn't look like a word anymore
class ScreenManager:
        
    screen : Screen
    possibleScreens : dict
    
    def __init__(self):
        screens = [Screen("Empty"), TableScreen("Table")]
        self.possibleScreens = {}
        
        for screen in screens:
            self.possibleScreens[screen.name] = screen
        
        self.screen = self.possibleScreens["Empty"]
        
    
    def request(self, screenName, data = []):
        if screenName != self.screen.name:
            self.screen = self.possibleScreens[screenName]
        
        if len(data) > 0:
            self.screen.update(data)
        
        self.screen.display()


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
