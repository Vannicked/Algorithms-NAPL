def displayTable(table : list):
    # should only take an array of strings as input
    tableLength = len(table)
    for i in range(tableLength):
        print(table[i])
    
    
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
    vertLine = "  | "
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


def fillEmptySpace(s : str, maxLength : int):
    inputLength = len(s)
    stringBuffer = s
    if inputLength > maxLength:
        raise ValueError("Max length of a column value is larger than input")
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


def main():
    tableHeader = ["Stock", "M1", "M2"]
    data = [tableHeader, ["AMC", 4.5, 7],["GME", 555, 6],["BBBYQ", 8, 999]]
    table = buildTable(data)
    displayTable(table)

main()