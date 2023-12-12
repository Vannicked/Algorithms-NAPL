from trader import Trader
from trader import Stock
import random
import ScreenManager

class GameManager:
    stockHeader = ["Stock", "M1", "M2", "M3", "M4", "M5", "M6"] # We'll need to implement a shifting date function
    data : list = []
    traders : list[Trader]
    currentTime : int
    timeframeStart : int
    timeframeEnd : int
    screenManager : ScreenManager.ScreenManager
    
    def __init__(self) -> None:
        self.screenManager = ScreenManager.ScreenManager()
    
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
        # More accurately maybe, we are getting the table for the current time.
        data = [self.stockHeader]
        for d in self.data:
            row = [d[0]] + d[(self.currentTime-5) : (self.currentTime + 1)] 
            data.append(row)
        return data

    def gameStart(self):
        gameRunning = True
        while gameRunning:
            self.progress()
            gameRunning = self.currentTime < self.timeframeEnd
        self.endGame()
                
    def updateHeader(self):
        self.stockHeader = ["Stock"]
        for i in range(self.currentTime-5, self.currentTime):
            month = f"M{i}"
            self.stockHeader.append(month)
        self.stockHeader.append(f"M{self.currentTime}(Now)")
    
    def progress(self):
        # flow of each turn: print stock table -> update stocks for traders -> traderAction -> updateTime
        turnNumber = self.currentTime - self.timeframeStart
        print("Turn " + str(turnNumber))
        if self.currentTime >= len(self.data[0]):
            raise IndexError("Current time has surpassed size of data.")

        self.updateHeader()
        stockData = self.getData()
        self.screenManager.request("StockTable", stockData)
        
        for t in self.traders:
            currTrader : Trader = t
            t.updateStocks(stockData)
            self.traderAction(currTrader) # Splits into player and bot
        self.currentTime = self.currentTime + 1
                    
    def endGame(self):
        print("Game over!")
        traderTable = [] 
        for t in self.traders:
            t.determineProfits()
            traderRow = [t.controller, t.capitalStart, t.capitalTotal, t.profit]
            traderTable.append(traderRow)
        self.screenManager.request("EndScreen", traderTable)
        self.askTraderHistory()
        print("Thanks for playing!")
        
    def askTraderHistory(self):
        print(f"You may look at the trade history of the players [1-{len(self.traders)}]")
        choosing = True
        another = "a"
        while choosing:
            choice = inputClean(f"Look at {another} trader's history? (Enter 0 to end program): ")
            try:
                choice = int(choice) - 1
                if choice == -1:
                    choosing = False
                else:
                    trader = self.traders[choice]
                    another = "another"
                    self.displayTraderHistory(trader)
            except:
                print(f"Please input a whole number between 1 and {len(self.traders)}, or 0 to choose none.")

                

    def displayTraderHistory(self, t : Trader):
        traderHistory = t.getHistory()
        for i in range(len(traderHistory)):
            traderHistory[i][0] += self.timeframeStart
        print(f"{t.controller}'s trading history:")
        self.screenManager.request("HistoryScreen", traderHistory)

    def traderAction(self, trader : Trader):
        if (trader.getController() == "Player"):
            print(f"Current Balance: {trader.balance}")
            choosing = True
            while choosing:
                self.screenManager.screenChange("StockTable")
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
                        print("Please input either b or s for buy or sell respectively, or n to progress time.")
        else:
            if trader.botAlgorithm == 1:
                self.botGreed(trader)
            elif trader.botAlgorithm == 2:
                self.botLong(trader)
            else:
                self.botGoldfish(trader)

    def inputAmount(self, max : int = 0):
        choosing = True
        while choosing:
            choice = inputClean("How many? ")
            try:
                choice = int(choice)
                return choice
            except:
                if max > 0:
                    print(f"Please input a number bewtween 0 and {max}")
                else:
                    print("Please input a whole number.")
                    

    # it is frustrating how messy all of this is, but if it works I'll be happy
    def buyStock(self, trader : Trader):
        if (trader.getController() == "Player"):
            choosing = True
            while choosing:
                choice = inputClean("Which stock to buy? ")
                try:
                    choice = int(choice) - 1
                    if choice == -1:
                        stockTup = None
                        choosing = False
                    else:
                        stockValue = self.data[choice][self.currentTime]
                        amount = self.inputAmount()
                        if (stockValue*amount) > trader.balance:
                            print(f"You can't afford to buy that much stock! Current Balance: {trader.balance}")
                        else:
                            stockTup = (self.data[choice][0], stockValue, amount)
                            choosing = self.verifyChoice(stockTup, 0)
                except:
                        print(f"Please input a whole number between 1 and {len(self.data)}, or 0 to choose none.")

        # Bot uses algorithm on data held by gm, does its search function that returns a stock (Name, Current Value)

        if stockTup != None:
            stockChoice : Stock = Stock(stockTup[0], stockTup[1], choice, stockTup[2])
            trader.buyStock(stockChoice)

    def sellStock(self, trader : Trader):
        # need to get the current value of the stock
        if (trader.getController() == "Player"):
            playerStockCount = len(trader.portfolio)
            choosing = (playerStockCount != 0)
            if not choosing:
                print("You have no stocks to sell!")
                return

            self.screenManager.request("TraderStocks", trader.getStocks())
            
            while choosing:
                choice = inputClean("Which stock to sell? ")
                try:
                    choice = int(choice) - 1
                    if choice == -1:
                        stockTup = None
                        choosing = False
                    else:
                        stock : Stock = trader.portfolio[choice]
                        amount = self.inputAmount(stock.amount)
                        if amount != 0:
                            stockTup = (stock.name, stock.currentValue, amount)
                            choosing = self.verifyChoice(stockTup, 1)
                except:
                        print(f"Please input a whole number between 1 and {len(trader.portfolio)}, or 0 to choose none.")
        
        if stockTup != None:
            trader.sellStock(choice, amount)

    def verifyChoice(self, choice, buySell : int):
        # should take the choice after choose stock is called
        if buySell == None:
            raise ValueError("BuySell has not been set properly")
        verifying = True
        bs = ("buy", "sell")
        while verifying:
            answer : str = inputClean(f"Are you sure you want to {bs[buySell]} {choice[2]} shares of {choice[0]} at {choice[1]}? [y/n] ")
            answer = answer.lower()
            if answer != 'y' and answer != 'n':
                print("Please input a valid answer [y/n].")
            else:
                return answer == 'n'
    
    def botGreed(self, trader : Trader):
        if len(trader.portfolio) == 0:
            maxInvestment = trader.balance
            index = 0
            for stock in self.data:
                s : Stock = Stock(stock[0], stock[1], index)
                index += 1
                if stock[1] <= maxInvestment:
                    trader.buyStock(s)
                    maxInvestment = maxInvestment - stock[1]
                else:
                    continue
        else:
            index = 0
            while len(trader.portfolio) > 0:
                trader.sellStock(0)
            maxInvestment = trader.balance
            for stock in self.data:
                s : Stock = Stock(stock[0], stock[1], index)
                index += 1
                if stock[1] <= maxInvestment:
                    trader.buyStock(s)
                    maxInvestment = maxInvestment - stock[1]
                else:
                    continue

    def botLong(self, trader : Trader):
        if len(trader.portfolio) == 0:
            index = 0
            maxInvestment = trader.balance / len(self.data)
            for stock in self.data:
                s : Stock = Stock(stock[0], stock[1], index)
                index += 1 
                if stock[1] <= maxInvestment and trader.balance >= stock[1]:
                    trader.buyStock(s)
                else:
                    continue
        else:
            while len(trader.portfolio) > 0:
                trader.sellStock(0)
            maxInvestment = trader.balance / len(self.data)
            index = 0
            for stock in self.data:
                s : Stock = Stock(stock[0], stock[1], index)
                index += 1
                if stock[1] <= maxInvestment and trader.balance >= stock[1]:
                    trader.buyStock(s) #adding stock needs to allow for selection of number of shares to add
                else:
                    continue

    def botGoldfish(self, trader : Trader):
        if len(trader.portfolio) == 0:
            maxInvestment = random.uniform(0, trader.balance)
            stockToBuy = random.randint(0, len(self.data) - 1)
            repeats = 0
            while repeats < len(self.data):
                s = Stock(self.data[stockToBuy][0], self.data[stockToBuy][1], stockToBuy)
                if s.currentValue > maxInvestment:
                    repeats = repeats + 1
                    stockToBuy = random.randint(0, len(self.data) - 1)
                    continue
                else:
                    flag = 0
                    for stock in trader.portfolio:
                        if s.buyIndex == stock.buyIndex:
                            repeats = repeats + 1
                            flag = 1
                            break
                        else:
                            continue
                    if flag == 0:
                        trader.buyStock(s)
                        maxInvestment -= s.currentValue
                        stockToBuy = random.randint(0, len(self.data) - 1)
                    else:
                        stockToBuy = random.randint(0, len(self.data) - 1)
        else:
            while len(trader.portfolio) > 0:
                trader.sellStock(0)
            maxInvestment = random.uniform(0, trader.balance)
            stockToBuy = random.randint(0, len(self.data) - 1)
            repeats = 0
            while repeats < len(self.data):
                s = Stock(self.data[stockToBuy][0], self.data[stockToBuy][1], stockToBuy)
                if s.currentValue > maxInvestment:
                    repeats = repeats + 1
                    stockToBuy = random.randint(0, len(self.data) - 1)
                    continue
                else:
                    flag = 0
                    for stock in trader.portfolio:
                        if s.buyIndex == stock.buyIndex:
                            repeats = repeats + 1
                            flag = 1
                            break
                        else:
                            continue
                    if flag == 0:
                        trader.buyStock(s)
                        maxInvestment -= s.currentValue
                        stockToBuy = random.randint(0, len(self.data) - 1)
                    else:
                        stockToBuy = random.randint(0, len(self.data) - 1)
                        


@staticmethod
def endTraderInfo(t : Trader):
    bufferString = f"{t.controller}:" + "\n" + f"- Starting Capital: {t.capitalStart}"+ \
                    "\n" + f"- Ending Capital: {t.capitalTotal}" + "\n" + f"- Profit: {t.profit}"
    print(bufferString)

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
    demoData = [["AMC", 4.5, 7, 10, 19, 17, 21, 22, 25, 23.5, 30.1, 28.4, 29], ["SHC", 2.1, 2, 2.4, 3.4, 3, 3.4, 3.2, 4.8, 5, 5.1, 5, 5.1], ["RGL", 32, 30, 26.2, 28.1, 28.4, 27.3, 25.9, 26.7, 24.3, 22, 21.3, 19.5]] # 18 months of values
    player = Trader("Player", playerBal, 0)
    botOne = Trader("Greedy Grinner", playerBal, 1)
    botTwo = Trader("Wise Guy", playerBal, 2)
    botThree = Trader("A Goldfish", playerBal, 3)
    traders = [player, botOne, botTwo, botThree]
    gameManager = GameManager() # time frame is set to 1 for now, because of how we read the data
    gameManager.sData(demoData).sTimeframe(6, 13).sTraders(traders)
    gameManager.gameStart()
    
main()