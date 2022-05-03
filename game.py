# imports
from deck import deck
from card import card

class game:
    """
    The Poker Game class.
    """
    def __init__(self,players) -> None:
        if len(players) < 2:
            print("Players needs to be two or more.")
            return Exception
        self.players = players
        self.activePlayers = players
        self.numOfPlayers = len(self.players)
        self.pot = 0
        self.call = 0
        self.deck = None
        self.shownCards = []
        self.history = []

    def newRound(self):
        """
        This method will begin a new turn/round and run until there is a winner.
        """
        # reset the numbers
        self.pot = 0
        self.call = 0
        self.nonFoldPlayers = self.numOfPlayers
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
        winner = False
        while(True):
            if (winner == False) and (self.activePlayers > 1):
                for index in range(len(self.players)):
                    if (self.players[index].getFoldStatus() == False):
                        turnResult = self.players[index].turn(self.call)
                        # evaluate the players actions and act accordinlgy
                        if (turnResult["action"] == "call"):
                            self.pot =+ self.call
                        elif (turnResult == "raise"):
                            self.raiseCall(amount=turnResult["amount"])
                            self.pot =+ self.call                
                        elif (turnResult == "fold"):
                            self.nonFoldPlayers =- 1
                            self.activePlayers.pop(self.players[index])
                    elif (len(self.activePlayers) == 1):
                        # declare this player as the winner and quit the round
                        currentPlayer = self.activePlayers[0]
                        print(f"The winner of this round is: {currentPlayer.getLabel()}")
                        currentPlayer.modifyChips(amount=self.pot)
                        winner = True
            elif (winner != False) or (self.activePlayers == 1):
                break
        # reset all player information
        for index in range(len(self.players)):
            self.players[index].resetState()
            



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
    
    def checkHands(self):
        """
        This method checks the hand of all active players and the cards on the table which are used to determine a winner.\n
        This method also changes the hand value for each player.
        """
        # this is the list of possible options
        handEvaluations =[ 
            {"type":"Royal Flush","value":10,"description":"Five highest cards of the same suit. Ace through ten."},
            {"type":"Straight Flush","value":9,"description":"Five cards of the same suit in order."},
            {"type":"Four Of A Kind","value":8,"description":"Four cards of the same rank."},
            {"type":"Full House","value":7,"description":"Two of a kind, along with three of a kind."},
            {"type":"Flush","value":6,"description":"Five cards of different ranks in the same suit."},
            {"type":"Straight","value":5,"description":"Five cards of different suits in order."},
            {"type":"Three Of A Kind","value":4,"description":"Three cards of the same kind."},
            {"type":"Two Pair","value":3,"description":"Two pairs, each with two cards of the same rank."},
            {"type":"Pair","value":2,"description":"Two cards of the same rank."},
            {"type":"High Card","value":1,"description":"Highest card in the game."}]
        # check the cards on the table with the 
        for index in range(len(self.activePlayers)):
            evalCards = self.shownCards
            evalCards.append(self.activePlayers[index].getCard())
            evalCards.append(self.activePlayers[index].getCard(2))
            evalCards.sort(key=lambda item: item.get("rank"))

