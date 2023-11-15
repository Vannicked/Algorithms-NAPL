import pandas as pd

class Stock:

    def __init__(self, name, value):
        self.name = name
        self.value = value #need to figure out if we want to include all values for the stock in this variable or just a single value

    def valueChange(self, newValue):
        self.value = newValue

class StockMarket:

    def __init__(self, stockOptions):
        self.stockOptions = pd.read_csv("StockPrices.csv")

class Bot:
    
    #initialize a new bot object, including the algorithm it uses for trading, the amount of money it has, and difficulty level
    def __init__(self, alg, diff, money, stocks):
        self.alg = alg #alg is an integer meant to represent a specific trading strategy that we implement
        self.diff = diff    #diff is the difficulty level that the bot is playing on
        self.money = money  #money is the amount of total money the bot has left after buying/selling
        self.stocks = stocks #stocks is a dictionary of stocks that the bot has invested in

    def greedy(self):
        #this function is the implementation of the greedy investment algorithm
        #dictionary to keep track of stock prices
        stock_prices = {}
        #stock prices in dictionary
        for stock in self.stocks:
            stock_prices[stock.name] = stock.value

        while self.money > 0:
            # stock with the lowest current value
            min_stock_name = min(stock_prices, key=stock_prices.get)

            # Check if the bot can afford to buy the stock
            if self.money >= stock_prices[min_stock_name]:
                # Buy stock
                self.money -= stock_prices[min_stock_name]
                print(f"Buying {min_stock_name} for {stock_prices[min_stock_name]}")
                # Update the bot's stocks list (need to implement this method)
                self.buy_stock(min_stock_name)
            else:
                # If the bot can't afford to buy any stock, break the loop
                break

            # Update the stock prices dictionary after the purchase
            stock_prices[min_stock_name] = stock_prices[min_stock_name] * 1.1  # Simulate price increase

        #print(f"Remaining money: {self.money}")
        #print("End of Greedy Algorithm")

    def longterm(self):
        #this function is the implementation of the long term investment algorithm
        #also utilizes a dictionary to track stock prices
        stock_prices = {}
        for stock in self.stocks:
            stock_prices[stock.name] = stock.value

    # Add a method to buy a stock and keep track of it
    def buy_stock(self, stock_name):
        for stock in self.stocks:
            if stock.name == stock_name:
                stock.valueChange(stock.value * 1.1)  # Simulate price increase
                # Implement the logic to keep track of the stocks bought
                # For example, you can maintain a list of bought stocks or update a data structure

    def invest(self):
        if (self.alg == 1):
            self.greedy()
        elif (self.alg == 2):
            #same for here
            print(self.alg)
        else:
            #same for here
            print(self.alg)