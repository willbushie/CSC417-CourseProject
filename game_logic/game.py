# imports
from deck import deck

class game:
    """
    The Poker Game class.
    """
    def __init__(self,players) -> None:
        if len(players) < 2:
            print("Players needs to be two or more.")
            return Exception
        self.players = players
        self.pot = 0
        self.call = 0
        self.deck = None
        self.shownCards = []
        self.history = []

    def newRound(self):
        """
        This method will begin a new turn/round.
        """
        # reset the numbers
        self.pot = 0
        self.call = 0
        # create deck
        self.deck = deck()
        # hand cards to players
        for index in len(range(self.players)):
            self.players[index].modifyHand(self.deck[0])
            self.deck.pop[0]
        for index in len(range(self.players)):
            self.players[index].modifyHand(self.deck[0])
            self.deck.pop[0]
        # for simplicty sake, start betting at self.players[0]
        for index in range(len(self.players)):
            turnResult = self.players[index].turn(self.call)
            # evaluate the players actions and act accordinlgy
            # add a loop to continue this process until and player wins



    def displayRoundStats(self):
        """
        This method will display the round stats, for each time a player is up to go.
        """
        print(f"Pot: {self.pot}, Current Call: {self.call}")
        if (len(self.shownCards) != 0):
            print("Revealed Cards:\n")
            for index in range(len(self.shownCards)):
                print(f"The {self.shownCards[index].getInfo()}\n")
    
    def raiseCall(self,amount):
        """
        This method is for when a player raises.
        """
        self.call =+ amount
    
