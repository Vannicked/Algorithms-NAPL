from trader import Trader
from trader import Stock
import random
import ScreenManager


class GameManager:
    stockHeader = ["Stock", "M1", "M2"] # We'll need to implement a shifting date function
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
        data = [self.stockHeader]
        for d in self.data:
            data.append(d)
        return data
    
    def gameStart(self):
        gameRunning = True
        while gameRunning:
            self.progress()
            gameRunning = self.currentTime < self.timeframeEnd
        self.endGame()
                
    def progress(self):
        # flow of each turn: print stock table -> update stocks for traders -> traderAction -> updateTime
        print("Turn " + str(self.currentTime - self.timeframeStart + 1))
        if self.currentTime >= len(self.data):
            raise IndexError("Current time has surpassed size of data.")

        stockData = self.getData()
        self.screenManager.request("StockTable", stockData)
        
        for t in self.traders:
            currTrader : Trader = t
            t.updateStocks(stockData)
            self.traderAction(currTrader) # Splits into player and bot
        self.currentTime = self.currentTime + 1
                    
    def endGame(self):
        print("Game over!")
        for t in self.traders:
            t.determineProfits()
            endTraderInfo(t)

    def traderAction(self, trader : Trader):
        if (trader.getController() == "Player"):
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
                        print("Please input either b or s for buy or sell respectively, or n to exit.")
        else:
            if trader.botAlgorithm == 1:
                self.botGreed(trader)
            elif trader.botAlgorithm == 2:
                self.botLong(trader)
            else:
                self.botGoldfish(trader)

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
                        if stockValue > trader.balance:
                            print(f"You can't afford to buy that stock! Current Balance: {trader.balance}")
                        else:
                            stockTup = (self.data[choice][0], stockValue)
                            choosing = self.verifyChoice(stockTup, 0)
                except:
                        print(f"Please input a whole number between 1 and {len(self.data)}, or 0 to choose none.")
        else:
            stockTup = ("something", 1)
        # Bot uses algorithm on data held by gm, does its search function that returns a stock (Name, Current Value)

        if stockTup != None:
            stockChoice : Stock = Stock(stockTup[0], stockTup[1], choice)
            trader.addStock(stockChoice)
            trader.updateBalance(-stockChoice.valueBought)

    def sellStock(self, trader : Trader):
        # need to get the current value of the stock
        if (trader.getController() == "Player"):
            playerStockCount = len(trader.portfolio)
            choosing = (playerStockCount != 0)
            if not choosing:
                print("You have no stocks to sell!")
                return

            # TODO: display currently owned stocks
            self.screenManager.request("TraderStocks", trader.getStocks())
            
            while choosing:
                choice = inputClean("Which stock to sell? ")
                try:
                    choice = int(choice) - 1
                    if choice == -1:
                        stockTup = None
                        choosing = False
                    else:
                        stockTup = (trader.portfolio[choice].name, self.data[trader.portfolio[choice].buyIndex][self.currentTime])
                        choosing = self.verifyChoice(stockTup, 1)
                except:
                        print(f"Please input a whole number between 1 and {len(trader.portfolio)}, or 0 to choose none.")
        
        if stockTup != None:
            stockChoice = trader.popStock(choice)
            trader.updateBalance(stockChoice.currentValue)

    def verifyChoice(self, choice, buySell : int):
        # should take the choice after choose stock is called
        if buySell == None:
            raise ValueError("BuySell has not been set properly")
        verifying = True
        bs = ("buy", "sell")
        while verifying:
            answer : str = inputClean(f"Are you sure you want to {bs[buySell]} {choice[0]} at {choice[1]}? [y/n] ")
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
                    trader.addStock(s)
                    trader.updateBalance(-stock[1])
                    maxInvestment = maxInvestment - stock[1]
                else:
                    continue
        else:
            index = 0
            while len(trader.portfolio) > 0:
                stock : Stock = trader.popStock(0)
                trader.updateBalance(stock.currentValue)
            maxInvestment = trader.balance
            for stock in self.data:
                s : Stock = Stock(stock[0], stock[1], index)
                index += 1
                if stock[1] <= maxInvestment:
                    trader.addStock(s)
                    trader.updateBalance(-stock[1])
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
                    trader.addStock(s)
                    trader.updateBalance(-stock[1])
                else:
                    continue
        else:
            while len(trader.portfolio) > 0:
                stock = trader.popStock(0)
                trader.updateBalance(stock.currentValue)
            maxInvestment = trader.balance / len(self.data)
            index = 0
            for stock in self.data:
                s : Stock = Stock(stock[0], stock[1], index)
                index += 1
                if stock[1] <= maxInvestment and trader.balance >= stock[1]:
                    trader.addStock(s) #adding stock needs to allow for selection of number of shares to add
                    trader.updateBalance(-stock[1])
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
                        trader.addStock(s)
                        trader.updateBalance(-s.currentValue)
                        maxInvestment -= s.currentValue
                        stockToBuy = random.randint(0, len(self.data) - 1)
                    else:
                        stockToBuy = random.randint(0, len(self.data) - 1)
        else:
            while len(trader.portfolio) > 0:
                stock = trader.popStock(0)
                trader.updateBalance(stock.currentValue)
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
                        trader.addStock(s)
                        trader.updateBalance(-s.currentValue)
                        maxInvestment -= s.currentValue
                        stockToBuy = random.randint(0, len(self.data) - 1)
                    else:
                        stockToBuy = random.randint(0, len(self.data) - 1)
                        


@staticmethod
def endTraderInfo(t : Trader):
    bufferString = f"{t.controller}:" + "\n" + f"Ending Capital: {t.capitalTotal}" + "\n" + f"Profit: {t.profit}"
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
    demoData = [] # 18 months of values
    player = Trader("Player", playerBal, 0)
    botOne = Trader("Greedy Lad", playerBal, 1)
    botTwo = Trader("Wise Guy", playerBal, 2)
    botThree = Trader("Silly Billy", playerBal, 3)
    traders = [player, botOne, botTwo, botThree]
    gameManager = GameManager() # time frame is set to 1 for now, because of how we read the data
    gameManager.sData(testData).sTimeframe(1, 3).sTraders(traders)
    gameManager.gameStart()
    
main()