class Trader:
    controller : str
    balance : float
    stocks : list = []
    
    def __init__(self, controller, balance) -> None:
        self.controller = controller
        self.balance = balance

    def getController(self):
        return self.controller