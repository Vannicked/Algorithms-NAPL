import pandas as pd
import trader

stock_options : pd.DataFrame = pd.read_csv("StockPrices.csv") #initialze a dataframe with all the data we need to access
date = 0 #this is the index of the row in which we are looking at values for data, and will be updated as the game progresses

class Bot(trader.Trader):
    
    #initialize a new bot object, including the algorithm it uses for trading, the amount of money it has, and difficulty level
    def __init__(self, controller, balance, alg):
        super.__init__(self, controller, balance)
        self.alg = alg #alg is an integer meant to represent a specific trading strategy that we implement
        self.stocks = {"AAL": 0,
                       "AAPL": 0,
                       "AMZN": 0,
                       "BAC": 0,
                       "DAL": 0,
                       "HMC": 0,
                       "JNJ": 0,
                       "JPM": 0,
                       "LLY": 0,
                       "LUV": 0,
                       "MSFT": 0,
                       "TM": 0,
                       "TSLA": 0,
                       "UNH": 0,
                       "V": 0} #stocks is a dictionary of stocks that the bot can invest in and updates according to the number of shares it holds

    def greedy(self):
        #this function is the implementation of the greedy investment algorithm
        #dictionary to keep track of stock prices
        stock_prices = {}
        #stock prices in dictionary
        for stock in self.stocks:
            stock_prices[stock.name] = stock.value

        while self.balance > 0:
            # stock with the lowest current value
            min_stock_name = min(stock_prices, key=stock_prices.get)

            # Check if the bot can afford to buy the stock
            if self.balance >= stock_prices[min_stock_name]:
                # Buy stock
                self.balance -= stock_prices[min_stock_name]
                print(f"Buying {min_stock_name} for {stock_prices[min_stock_name]}")
                # Update the bot's stocks list (need to implement this method)
                self.buy_stock(min_stock_name)
            else:
                # If the bot can't afford to buy any stock, break the loop
                break

            # Update the stock prices dictionary after the purchase
            stock_prices[min_stock_name] = stock_prices[min_stock_name] * 1.1  # Simulate price increase

        #print(f"Remaining balance: {self.balance}")
        #print("End of Greedy Algorithm")

    def longterm(self):
        #this function is the implementation of the long term investment algorithm
        if date != 0:
            for key in self.stocks:
                self.sell_stock(key)
            for key in self.stocks:
                if (self.balance > stock_options[date][key]):
                    self.buy_stock(key, 5)
        else:
            for key in self.stocks:
                if (self.balance > stock_options[date][key]):
                    self.buy_stock(key, 5)


        print("longterm")

    def goldfish(self):
        print("goldfish")

    # Add a method to buy a stock and keep track of it
    def buy_stock(self, stock_name, shares):
        self.stocks.update[stock_name] = shares
        self.balance = self.balance - (stock_options[date][stock_name] * shares)

    def sell_stock(self, stock_name):
        self.balance = self.balance + (stock_options[date][stock_name] * self.stocks[stock_name])
        self.stocks[stock_name] = 0

    def invest(self):
        if (self.alg == 1):
            self.greedy()
        elif (self.alg == 2):
            self.longterm()
        else:
            self.goldfish()