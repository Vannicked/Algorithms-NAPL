class Stock:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def valueChange(self, newValue):
        self.value = newValue

class Bot:
    
    #initialize a new bot object, including the algorithm it uses for trading, the amount of money it has, and difficulty level
    def __init__(self, alg, diff, money, stocks):
        self.alg = alg #alg is an integer meant to represent a specific trading strategy that we implement
        self.diff = diff    #diff is the difficulty level that the bot is playing on
        self.money = money  #money is the amount of total money the bot has left after buying/selling
        self.stocks = stocks #stocks is an array of stock options (need to hardcode indices in order to reference number of stocks purchased)

    def invest(self):
        if (self.alg == 1):
            #insert whatever trading algorithm is the first one we come up with
            print(self.alg)
        elif (self.alg == 2):
            #same for here
            print(self.alg)
        else:
            #same for here
            print(self.alg)

    def greedy(self):
        #this function is the implementation of the greedy investment algorithm
        print("greed")