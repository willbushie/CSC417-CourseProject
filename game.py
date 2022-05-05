# imports
from deck import deck
from card import card

class game:
    """
    The Poker Game class.
    """
    def __init__(self,players,call,play=True,cards=None):
        if (len(players) < 2) and (play == True):
            print("Number of players needs to be two or more.")
            return Exception # change this to something that makes more sense
        self.players = players
        self.activePlayers = players
        self.call = call
        self.history = []
        # play the game
        if (play == True):
            # needs to be a better way of continueing a game until:
            # 1) only on player remains (because players quit)
            # 2) one player wins (only player with chips)
            self.newRound()
        # test evaluateHands Function
        elif (play == False):
            self.evaluateHands(cards,players)

    def newRound(self):
        """
        This method will begin a new turn/round and run until there is a winner/one remaining player (e.i. everyone else folded).
        """
        # reset the numbers & prepare state
        pot = 0
        call = self.call
        previousCall = self.call
        anti = self.call
        shownCards = []
        activePlayers = self.activePlayers
        currDeck = deck()
        # hand cards to players
        for index in range(len(self.activePlayers)):
            self.activePlayers[index].modifyHand(currDeck.getCardAtIndex())
            currDeck.removeCardAt()
        for index in range(len(self.activePlayers)):
            self.activePlayers[index].modifyHand(currDeck.getCardAtIndex())
            currDeck.removeCardAt()
        # start the betting round
        print("/// A new round has started ///")
        # have all players place the anti
        for index in range(len(activePlayers)):
            activePlayers[index].modifyChips(anti)
            pot = pot + anti
        print("/// All players have paid the anti ///")
        # start the entire round (until there is a winner/or/only one person has not folded)
        while(len(activePlayers) != 1):
            while((self.allPlayersBet(activePlayers) == False)):
                # begin asking players to take their turns
                for p in activePlayers:
                    print("===============================")
                    if (len(activePlayers) != 1):
                        print(f"Current Pot value: {pot}. Player {p.getLabel()} is betting.")
                        if (len(shownCards) != 0):
                            print(f"The current table cards are: {self.prettyPrintShownCards(shownCards)}.")
                        if (previousCall != call):
                            currPlayerResult = p.turn(call)
                        elif (previousCall == call):
                            currPlayerResult = p.turn(0)
                        # if a player checks, modify call status, and move on
                        if (currPlayerResult["action"] == "check"):
                            print(f"Player {p.getLabel()} has checked. Remaining chips: {p.getChipValue()}. Moving to next player.")
                            p.modifyCallStatus(status=True)
                        # if a player calls, modify their call status and move on
                        elif (currPlayerResult["action"] == "call"):
                            print(f"Player {p.getLabel()} has called. Remaining chips: {p.getChipValue()}. Moving to next player.")
                            p.modifyCallStatus(status=True)
                        # if a player raises, modify their call status, and modify everyone elses to False
                        elif (currPlayerResult["action"] == "raise"):
                            print(f"Player {p.getLabel()} has raised by {currPlayerResult['amount']}. Remaining chips: {p.getChipValue()}. Moving to next player.")
                            pot = pot + currPlayerResult["amount"]
                            call = currPlayerResult["amount"]
                            for index in range(len(activePlayers)):
                                p.modifyCallStatus()
                            p.modifyCallStatus(status=True)
                        # if a player folds, remove them from active players for the round (not self.active players)
                        elif (currPlayerResult["action"] == "fold"):
                            print(f"Player {p.getLabel()} has folded.")
                            activePlayers.remove(p)
                    elif (len(activePlayers) == 1):
                        break
                previousCall = call
            # once all players' call status is True, move on (flop, fourth deal, river)
            if (len(shownCards) == 0) and (len(activePlayers) > 1) and (self.allPlayersBet(activePlayers) == True):
                for i in range(3):
                    shownCards.append(currDeck.getCardAtIndex(0))
                    currDeck.removeCardAt(0)
                print(f"Betting has finished, the flop is: {self.prettyPrintShownCards(shownCards)}")
            elif (len(shownCards) == 3) and (len(activePlayers) > 1) and (self.allPlayersBet(activePlayers) == True):
                shownCards.append(currDeck.getCardAtIndex(0))
                currDeck.removeCardAt(0)
                print(f"Betting has finished, the turn is: {self.prettyPrintShownCards(shownCards)}")
            elif (len(shownCards) == 4) and (len(activePlayers) > 1) and (self.allPlayersBet(activePlayers) == True):
                shownCards.append(currDeck.getCardAtIndex(0))
                currDeck.removeCardAt(0)
                print(f"Betting has finished, the river is: {self.prettyPrintShownCards(shownCards)}")
            elif (len(shownCards) == 5) and (self.allPlayersBet(activePlayers) == True):
                break
            for index in range(len(activePlayers)):
                p.modifyCallStatus()
        # evaluate the players left or move winning to the single player that is left
        if (len(activePlayers) == 1):
            activePlayers[0].modifyChips(amount=pot,transactionType=1)
            print(f"Player {activePlayers[0].getLabel()} has won the round. Winnings: {pot}. Chips: {activePlayers[0].getChipValue()}")
        elif(len(activePlayers) > 1):
            self.evaluateHands(shownCards,activePlayers)
            # select the winning player
            scores = []
            for index in range(len(activePlayers)):
                scores.append(activePlayers[index].getHandValue()["score"])
            maxScore = max(scores)
            winningPlayers = []
            for index in range(len(activePlayers)):
                if (activePlayers[index].getHandValue()["score"] == maxScore):
                    winningPlayers.append(activePlayers[index])
            if (len(winningPlayers) == 1):
                winningPlayers[0].modifyChips(pot,transactiontype=1)
                print(f"Player {winningPlayers[index].getLabel()} has won the round. Winnings: {pot}. Chips: {activePlayers[index].getChipValue()}")
            elif (len(winningPlayers) > 1):
                for index in range(len(winningPlayers)):
                    winningPlayers[index].modifyChips((pot/len(winningPlayers)),transactionType=1)
                    print(f"Player {winningPlayers[index].getLabel()} has tied for the win. Winnings: {pot/len(winningPlayers)}. Chips: {activePlayers[index].getChipValue()}")
        # ensure a player is removed from the self.players list if their chips are 0
        index = 0
        while(index < len(self.activePlayers)):
            if (self.activePlayers[index].getChipValue() == 0):
                self.activePlayers.pop(index)
                index = index - 1
            index = index + 1
        # shuffle players inside of self.activePlayers (move first player to end, and all players up one [1,2,3,4] > [2,3,4,1])
        firstPlayer = self.activePlayers[0]
        self.activePlayers.pop(0)
        self.activePlayers.append(firstPlayer)
        # reset all player information
        for index in range(len(self.players)):
            self.players[index].resetState()

    
    def allPlayersBet(self,activePlayers):
        """
        This method will check if all players in an active player's list have bet or not. Returns `False` if not and `True` if yes.
        """
        numOfPlayers = len(activePlayers)
        betCount = 0
        for index in range(len(activePlayers)):
            if (activePlayers[index].getCallStatus() == True):
                betCount = betCount + 1
        if (numOfPlayers == betCount):
            return True
        elif (numOfPlayers != betCount):
            return False
    
    def cardInList(self,list,rank,suit):
        """
        This method returns a true or false, on whether the card is present in the passed list or not.
        """
        integerList = ["1","2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace"]
        alphabeticalList = ["One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King","Ace"]
        for c in list:
            if (rank in integerList):
                if (c.getRank() == alphabeticalList[integerList.index(rank)]) and (c.getSuit() == suit):
                    return True
            elif (rank in alphabeticalList):
                if (c.getRank() == rank) and (c.getSuit() == suit):
                    return True
        return False


    def prettyPrintShownCards(self,cards):
        """
        This method prints a cleanly formatted string of the shown cards.
        """
        hold = ""
        for i in range(len(cards)):
            hold = hold + cards[i].getInfo()
            if (i < len(cards) - 1):
                hold = hold + ", "
        return hold

    def evaluateHands(self,tableCards,players):
        """
        This method checks the hand of all active players and the cards on the table which are used to determine a winner.
        This method also changes the hand value for each player.
        The card handing checking is not perfect, but it functions correclty.
        """
        # check the cards on the table with the 
        for index in range(len(players)):
            evalCards = tableCards
            evalCards.append(players[index].getCard())
            evalCards.append(players[index].getCard(2))
            evalCards.sort(key=lambda item: item.getRank())
            
            stats = {"d":0,"h":0,"c":0,"s":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"Jack":0,"Queen":0,"King":0,"Ace":0}
            # update stats
            for i in range(len(evalCards)):
                currCard = evalCards[i]
                suit = currCard.getSuit()
                rank = currCard.getRank()
                # checking suits
                if (suit == "Hearts"):
                    stats["h"] = stats["h"] + 1
                elif (suit == "Diamonds"):
                    stats["d"] = stats["d"] + 1
                elif (suit == "Clubs"):
                    stats["c"] = stats["c"] + 1
                elif (suit == "Spades"):
                    stats["s"] = stats["s"] + 1
                # checking rank
                if (rank == "One"):
                    stats["1"] = stats["1"] + 1
                elif (rank == "Two"):
                    stats["2"] = stats["2"] + 1
                elif (rank == "Three"):
                    stats["3"] = stats["3"] + 1
                elif (rank == "Four"):
                    stats["4"] = stats["4"] + 1
                elif (rank == "Five"):
                    stats["5"] = stats["5"] + 1
                elif (rank == "Six"):
                    stats["6"] = stats["6"] + 1
                elif (rank == "Seven"):
                    stats["7"] = stats["7"] + 1
                elif (rank == "Eight"):
                    stats["8"] = stats["8"] + 1
                elif (rank == "Nine"):
                    stats["9"] = stats["9"] + 1
                elif (rank == "Ten"):
                    stats["10"] = stats["10"] + 1
                elif (rank == "Jack"):
                    stats["Jack"] = stats["Jack"] + 1
                elif (rank == "Queen"):
                    stats["Queen"] = stats["Queen"] + 1
                elif (rank == "King"):
                    stats["King"] = stats["King"] + 1
                elif (rank == "Ace"):
                    stats["Ace"] = stats["Ace"] + 1

            # 10 - checking for royal flush (5 highest cards of the same suit)
            if (stats["10"] >= 1) and (stats["Jack"] >= 1) and (stats["Queen"] >= 1) and (stats["King"] >= 1) and (stats["Ace"] >= 1):
                if (self.cardInList(evalCards,"10","Clubs") == True) and (self.cardInList(evalCards,"Jack","Clubs") == True) and (self.cardInList(evalCards,"Queen","Clubs") == True) and (self.cardInList(evalCards,"King","Clubs") == True) and (self.cardInList(evalCards,"Ace","Clubs") == True):
                    players[index].modifyHandValue(score=10)
                elif (self.cardInList(evalCards,"10","Hearts") == True) and (self.cardInList(evalCards,"Jack","Hearts") == True) and (self.cardInList(evalCards,"Queen","Hearts") == True) and (self.cardInList(evalCards,"King","Hearts") == True) and (self.cardInList(evalCards,"Ace","Hearts") == True):
                    players[index].modifyHandValue(score=10)
                elif (self.cardInList(evalCards,"10","Diamonds") == True) and (self.cardInList(evalCards,"Jack","Diamonds") == True) and (self.cardInList(evalCards,"Queen","Diamonds") == True) and (self.cardInList(evalCards,"King","Diamonds") == True) and (self.cardInList(evalCards,"Ace","Diamonds") == True):
                    players[index].modifyHandValue(score=10)
                elif (self.cardInList(evalCards,"10","Spades") == True) and (self.cardInList(evalCards,"Jack","Spades") == True) and (self.cardInList(evalCards,"Queen","Spades") == True) and (self.cardInList(evalCards,"King","Spades") == True) and (self.cardInList(evalCards,"Ace","Spades") == True):
                    players[index].modifyHandValue(score=10)
            
            # 9  - checking for straight flush (five cards of the same suit in order)
            if (stats["Ace"] >= 1) and (stats["1"] >= 1) and (stats["2"] >= 1) and (stats["3"] >= 1) and (stats["4"] >= 1):
                if (self.cardInList(evalCards,"Ace","Clubs") == True) and (self.cardInList(evalCards,"1","Clubs") == True) and (self.cardInList(evalCards,"2","Clubs") == True) and (self.cardInList(evalCards,"3","Clubs") == True) and (self.cardInList(evalCards,"4","Clubs") == True):
                    players[index].modifyHandValue(score=9,value=0)
                elif (self.cardInList(evalCards,"Ace","Diamonds") == True) and (self.cardInList(evalCards,"1","Diamonds") == True) and (self.cardInList(evalCards,"2","Diamonds") == True) and (self.cardInList(evalCards,"3","Diamonds") == True) and (self.cardInList(evalCards,"4","Diamonds") == True):
                    players[index].modifyHandValue(score=9,value=0)
                elif (self.cardInList(evalCards,"Ace","Hearts") == True) and (self.cardInList(evalCards,"1","Hearts") == True) and (self.cardInList(evalCards,"2","Hearts") == True) and (self.cardInList(evalCards,"3","Hearts") == True) and (self.cardInList(evalCards,"4","Hearts") == True):
                    players[index].modifyHandValue(score=9,value=0)
                elif (self.cardInList(evalCards,"Ace","Spades") == True) and (self.cardInList(evalCards,"1","Spades") == True) and (self.cardInList(evalCards,"2","Spades") == True) and (self.cardInList(evalCards,"3","Spades") == True) and (self.cardInList(evalCards,"4","Spades") == True):
                    players[index].modifyHandValue(score=9,value=0)
            if (stats["1"] >= 1) and (stats["2"] >= 1) and (stats["3"] >= 1) and (stats["4"] >= 1) and (stats["5"] >= 1):
                if (self.cardInList(evalCards,"1","Clubs") == True) and (self.cardInList(evalCards,"2","Clubs") == True) and (self.cardInList(evalCards,"3","Clubs") == True) and (self.cardInList(evalCards,"4","Clubs") == True) and (self.cardInList(evalCards,"5","Clubs") == True):
                    players[index].modifyHandValue(score=9,value=1)
                elif (self.cardInList(evalCards,"1","Diamonds") == True) and (self.cardInList(evalCards,"2","Diamonds") == True) and (self.cardInList(evalCards,"3","Diamonds") == True) and (self.cardInList(evalCards,"4","Diamonds") == True) and (self.cardInList(evalCards,"5","Diamonds") == True):
                    players[index].modifyHandValue(score=9,value=1)
                elif (self.cardInList(evalCards,"1","Hearts") == True) and (self.cardInList(evalCards,"2","Hearts") == True) and (self.cardInList(evalCards,"3","Hearts") == True) and (self.cardInList(evalCards,"4","Hearts") == True) and (self.cardInList(evalCards,"5","Hearts") == True):
                    players[index].modifyHandValue(score=9,value=1)
                elif (self.cardInList(evalCards,"1","Spades") == True) and (self.cardInList(evalCards,"2","Spades") == True) and (self.cardInList(evalCards,"3","Spades") == True) and (self.cardInList(evalCards,"4","Spades") == True) and (self.cardInList(evalCards,"5","Spades") == True):
                    players[index].modifyHandValue(score=9,value=1)
            elif (stats["2"] >= 1) and (stats["3"] >= 1) and (stats["4"] >= 1) and (stats["5"] >= 1) and (stats["6"] >= 1):
                if (self.cardInList(evalCards,"2","Clubs") == True) and (self.cardInList(evalCards,"3","Clubs") == True) and (self.cardInList(evalCards,"4","Clubs") == True) and (self.cardInList(evalCards,"5","Clubs") == True) and (self.cardInList(evalCards,"6","Clubs") == True):
                    players[index].modifyHandValue(score=9,value=2)
                elif (self.cardInList(evalCards,"2","Diamonds") == True) and (self.cardInList(evalCards,"3","Diamonds") == True) and (self.cardInList(evalCards,"4","Diamonds") == True) and (self.cardInList(evalCards,"5","Diamonds") == True) and (self.cardInList(evalCards,"6","Diamonds") == True):
                    players[index].modifyHandValue(score=9,value=2)
                elif (self.cardInList(evalCards,"2","Hearts") == True) and (self.cardInList(evalCards,"3","Hearts") == True) and (self.cardInList(evalCards,"4","Hearts") == True) and (self.cardInList(evalCards,"5","Hearts") == True) and (self.cardInList(evalCards,"6","Hearts") == True):
                    players[index].modifyHandValue(score=9,value=2)
                elif (self.cardInList(evalCards,"2","Spades") == True) and (self.cardInList(evalCards,"3","Spades") == True) and (self.cardInList(evalCards,"4","Spades") == True) and (self.cardInList(evalCards,"5","Spades") == True) and (self.cardInList(evalCards,"6","Spades") == True):
                    players[index].modifyHandValue(score=9,value=2)
            elif (stats["3"] >= 1) and (stats["4"] >= 1) and (stats["5"] >= 1) and (stats["6"] >= 1) and (stats["7"] >= 1):
                if (self.cardInList(evalCards,"3","Clubs") == True) and (self.cardInList(evalCards,"4","Clubs") == True) and (self.cardInList(evalCards,"5","Clubs") == True) and (self.cardInList(evalCards,"6","Clubs") == True) and (self.cardInList(evalCards,"7","Clubs") == True):
                    players[index].modifyHandValue(score=9,value=3)
                elif (self.cardInList(evalCards,"3","Diamonds") == True) and (self.cardInList(evalCards,"4","Diamonds") == True) and (self.cardInList(evalCards,"5","Diamonds") == True) and (self.cardInList(evalCards,"6","Diamonds") == True) and (self.cardInList(evalCards,"7","Diamonds") == True):
                    players[index].modifyHandValue(score=9,value=3)
                elif (self.cardInList(evalCards,"3","Hearts") == True) and (self.cardInList(evalCards,"4","Hearts") == True) and (self.cardInList(evalCards,"5","Hearts") == True) and (self.cardInList(evalCards,"6","Hearts") == True) and (self.cardInList(evalCards,"7","Hearts") == True):
                    players[index].modifyHandValue(score=9,value=3)
                elif (self.cardInList(evalCards,"3","Spades") == True) and (self.cardInList(evalCards,"4","Spades") == True) and (self.cardInList(evalCards,"5","Spades") == True) and (self.cardInList(evalCards,"6","Spades") == True) and (self.cardInList(evalCards,"7","Spades") == True):
                    players[index].modifyHandValue(score=9,value=3)
            elif (stats["4"] >= 1) and (stats["5"] >= 1) and (stats["6"] >= 1) and (stats["7"] >= 1) and (stats["8"] >= 1):
                if (self.cardInList(evalCards,"4","Clubs") == True) and (self.cardInList(evalCards,"5","Clubs") == True) and (self.cardInList(evalCards,"6","Clubs") == True) and (self.cardInList(evalCards,"7","Clubs") == True) and (self.cardInList(evalCards,"8","Clubs") == True):
                    players[index].modifyHandValue(score=9,value=4)
                elif (self.cardInList(evalCards,"4","Diamonds") == True) and (self.cardInList(evalCards,"5","Diamonds") == True) and (self.cardInList(evalCards,"6","Diamonds") == True) and (self.cardInList(evalCards,"7","Diamonds") == True) and (self.cardInList(evalCards,"8","Diamonds") == True):
                    players[index].modifyHandValue(score=9,value=4)
                elif (self.cardInList(evalCards,"4","Hearts") == True) and (self.cardInList(evalCards,"5","Hearts") == True) and (self.cardInList(evalCards,"6","Hearts") == True) and (self.cardInList(evalCards,"7","Hearts") == True) and (self.cardInList(evalCards,"8","Hearts") == True):
                    players[index].modifyHandValue(score=9,value=4)
                elif (self.cardInList(evalCards,"4","Spades") == True) and (self.cardInList(evalCards,"5","Spades") == True) and (self.cardInList(evalCards,"6","Spades") == True) and (self.cardInList(evalCards,"7","Spades") == True) and (self.cardInList(evalCards,"8","Spades") == True):
                    players[index].modifyHandValue(score=9,value=4)
            elif (stats["5"] >= 1) and (stats["6"] >= 1) and (stats["7"] >= 1) and (stats["8"] >= 1) and (stats["9"] >= 1):
                if (self.cardInList(evalCards,"5","Clubs") == True) and (self.cardInList(evalCards,"6","Clubs") == True) and (self.cardInList(evalCards,"7","Clubs") == True) and (self.cardInList(evalCards,"8","Clubs") == True) and (self.cardInList(evalCards,"9","Clubs") == True):
                    players[index].modifyHandValue(score=9,value=5)
                elif (self.cardInList(evalCards,"5","Diamonds") == True) and (self.cardInList(evalCards,"6","Diamonds") == True) and (self.cardInList(evalCards,"7","Diamonds") == True) and (self.cardInList(evalCards,"8","Diamonds") == True) and (self.cardInList(evalCards,"9","Diamonds") == True):
                    players[index].modifyHandValue(score=9,value=5)
                elif (self.cardInList(evalCards,"5","Hearts") == True) and (self.cardInList(evalCards,"6","Hearts") == True) and (self.cardInList(evalCards,"7","Hearts") == True) and (self.cardInList(evalCards,"8","Hearts") == True) and (self.cardInList(evalCards,"9","Hearts") == True):
                    players[index].modifyHandValue(score=9,value=5)
                elif (self.cardInList(evalCards,"5","Spades") == True) and (self.cardInList(evalCards,"6","Spades") == True) and (self.cardInList(evalCards,"7","Spades") == True) and (self.cardInList(evalCards,"8","Spades") == True) and (self.cardInList(evalCards,"9","Spades") == True):
                    players[index].modifyHandValue(score=9,value=5)
            elif (stats["6"] >= 1) and (stats["7"] >= 1) and (stats["8"] >= 1) and (stats["9"] >= 1) and (stats["10"] >= 1):
                if (self.cardInList(evalCards,"6","Clubs") == True) and (self.cardInList(evalCards,"7","Clubs") == True) and (self.cardInList(evalCards,"8","Clubs") == True) and (self.cardInList(evalCards,"9","Clubs") == True) and (self.cardInList(evalCards,"10","Clubs") == True):
                    players[index].modifyHandValue(score=9,value=6)
                elif (self.cardInList(evalCards,"6","Diamonds") == True) and (self.cardInList(evalCards,"7","Diamonds") == True) and (self.cardInList(evalCards,"8","Diamonds") == True) and (self.cardInList(evalCards,"9","Diamonds") == True) and (self.cardInList(evalCards,"10","Diamonds") == True):
                    players[index].modifyHandValue(score=9,value=6)
                elif (self.cardInList(evalCards,"6","Hearts") == True) and (self.cardInList(evalCards,"7","Hearts") == True) and (self.cardInList(evalCards,"8","Hearts") == True) and (self.cardInList(evalCards,"9","Hearts") == True) and (self.cardInList(evalCards,"10","Hearts") == True):
                    players[index].modifyHandValue(score=9,value=6)
                elif (self.cardInList(evalCards,"6","Spades") == True) and (self.cardInList(evalCards,"7","Spades") == True) and (self.cardInList(evalCards,"8","Spades") == True) and (self.cardInList(evalCards,"9","Spades") == True) and (self.cardInList(evalCards,"10","Spades") == True):
                    players[index].modifyHandValue(score=9,value=6)
            elif (stats["7"] >= 1) and (stats["8"] >= 1) and (stats["9"] >= 1) and (stats["10"] >= 1) and (stats["Jack"] >= 1):
                if (self.cardInList(evalCards,"7","Clubs") == True) and (self.cardInList(evalCards,"8","Clubs") == True) and (self.cardInList(evalCards,"9","Clubs") == True) and (self.cardInList(evalCards,"10","Clubs") == True) and (self.cardInList(evalCards,"Jack","Clubs") == True):
                    players[index].modifyHandValue(score=9,value=7)
                elif (self.cardInList(evalCards,"7","Diamonds") == True) and (self.cardInList(evalCards,"8","Diamonds") == True) and (self.cardInList(evalCards,"9","Diamonds") == True) and (self.cardInList(evalCards,"10","Diamonds") == True) and (self.cardInList(evalCards,"Jack","Diamonds") == True):
                    players[index].modifyHandValue(score=9,value=7)
                elif (self.cardInList(evalCards,"7","Hearts") == True) and (self.cardInList(evalCards,"8","Hearts") == True) and (self.cardInList(evalCards,"9","Hearts") == True) and (self.cardInList(evalCards,"10","Hearts") == True) and (self.cardInList(evalCards,"Jack","Hearts") == True):
                    players[index].modifyHandValue(score=9,value=7)
                elif (self.cardInList(evalCards,"7","Spades") == True) and (self.cardInList(evalCards,"8","Spades") == True) and (self.cardInList(evalCards,"9","Spades") == True) and (self.cardInList(evalCards,"10","Spades") == True) and (self.cardInList(evalCards,"Jack","Spades") == True):
                    players[index].modifyHandValue(score=9,value=7)
            elif (stats["8"] >= 1) and (stats["9"] >= 1) and (stats["10"] >= 1) and (stats["Jack"] >= 1) and (stats["Queen"] >= 1):
                if (self.cardInList(evalCards,"8","Clubs") == True) and (self.cardInList(evalCards,"9","Clubs") == True) and (self.cardInList(evalCards,"10","Clubs") == True) and (self.cardInList(evalCards,"Jack","Clubs") == True) and (self.cardInList(evalCards,"Queen","Clubs") == True):
                    players[index].modifyHandValue(score=9,value=8)
                elif (self.cardInList(evalCards,"8","Diamonds") == True) and (self.cardInList(evalCards,"9","Diamonds") == True) and (self.cardInList(evalCards,"10","Diamonds") == True) and (self.cardInList(evalCards,"Jack","Diamonds") == True) and (self.cardInList(evalCards,"Queen","Diamonds") == True):
                    players[index].modifyHandValue(score=9,value=8)
                elif (self.cardInList(evalCards,"8","Hearts") == True) and (self.cardInList(evalCards,"9","Hearts") == True) and (self.cardInList(evalCards,"10","Hearts") == True) and (self.cardInList(evalCards,"Jack","Hearts") == True) and (self.cardInList(evalCards,"Queen","Hearts") == True):
                    players[index].modifyHandValue(score=9,value=8)
                elif (self.cardInList(evalCards,"8","Spades") == True) and (self.cardInList(evalCards,"9","Spades") == True) and (self.cardInList(evalCards,"10","Spades") == True) and (self.cardInList(evalCards,"Jack","Spades") == True) and (self.cardInList(evalCards,"Queen","Spades") == True):
                    players[index].modifyHandValue(score=9,value=8)
            elif (stats["9"] >= 1) and (stats["10"] >= 1) and (stats["Jack"] >= 1) and (stats["Queen"] >= 1) and (stats["King"] >= 1):
                if (self.cardInList(evalCards,"9","Clubs") == True) and (self.cardInList(evalCards,"10","Clubs") == True) and (self.cardInList(evalCards,"Jack","Clubs") == True) and (self.cardInList(evalCards,"Queen","Clubs") == True) and (self.cardInList(evalCards,"King","Clubs") == True):
                    players[index].modifyHandValue(score=9,value=9)
                elif (self.cardInList(evalCards,"9","Diamonds") == True) and (self.cardInList(evalCards,"10","Diamonds") == True) and (self.cardInList(evalCards,"Jack","Diamonds") == True) and (self.cardInList(evalCards,"Queen","Diamonds") == True) and (self.cardInList(evalCards,"King","Diamonds") == True):
                    players[index].modifyHandValue(score=9,value=9)
                elif (self.cardInList(evalCards,"9","Hearts") == True) and (self.cardInList(evalCards,"10","Hearts") == True) and (self.cardInList(evalCards,"Jack","Hearts") == True) and (self.cardInList(evalCards,"Queen","Hearts") == True) and (self.cardInList(evalCards,"King","Hearts") == True):
                    players[index].modifyHandValue(score=9,value=9)
                elif (self.cardInList(evalCards,"9","Spades") == True) and (self.cardInList(evalCards,"10","Spades") == True) and (self.cardInList(evalCards,"Jack","Spades") == True) and (self.cardInList(evalCards,"Queen","Spades") == True) and (self.cardInList(evalCards,"King","Spades") == True):
                    players[index].modifyHandValue(score=9,value=9)
            
            # 8  - checking for four of a kind
            if (stats["1"] == 4):
                players[index].modifyHandValue(score=8,value=0)
            elif (stats["2"] == 4):
                players[index].modifyHandValue(score=8,value=1)
            elif (stats["3"] == 4):
                players[index].modifyHandValue(score=8,value=2)
            elif (stats["4"] == 4):
                players[index].modifyHandValue(score=8,value=3)
            elif (stats["5"] == 4):
                players[index].modifyHandValue(score=8,value=4)
            elif (stats["6"] == 4):
                players[index].modifyHandValue(score=8,value=5)
            elif (stats["7"] == 4):
                players[index].modifyHandValue(score=8,value=6)
            elif (stats["8"] == 4):
                players[index].modifyHandValue(score=8,value=7)
            elif (stats["9"] == 4):
                players[index].modifyHandValue(score=8,value=8)
            elif (stats["10"] == 4):
                players[index].modifyHandValue(score=8,value=9)
            elif (stats["Jack"] == 4):
                players[index].modifyHandValue(score=8,value=10)
            elif (stats["Queen"] == 4):
                players[index].modifyHandValue(score=8,value=11)
            elif (stats["King"] == 4):
                players[index].modifyHandValue(score=8,value=12)
            elif (stats["Ace"] == 4):
                players[index].modifyHandValue(score=8,value=13)
            
            # 7  - checking for a full house (one pair, and one three of a kind)
            if (stats["1"] == 3):
                if (stats["2"] >= 2):
                    players[index].modifyHand(score=7,value=(0+1))
                elif (stats["3"] >= 2):
                    players[index].modifyHand(score=7,value=(0+2))
                elif (stats["4"] >= 2):
                    players[index].modifyHand(score=7,value=(0+3))
                elif (stats["5"] >= 2):
                    players[index].modifyHand(score=7,value=(0+4))
                elif (stats["6"] >= 2):
                    players[index].modifyHand(score=7,value=(0+5))
                elif (stats["7"] >= 2):
                    players[index].modifyHand(score=7,value=(0+6))
                elif (stats["8"] >= 2):
                    players[index].modifyHand(score=7,value=(0+7))
                elif (stats["9"] >= 2):
                    players[index].modifyHand(score=7,value=(0+8))
                elif (stats["10"] >= 2):
                    players[index].modifyHand(score=7,value=(0+9))
                elif (stats["Jack"] >= 2):
                    players[index].modifyHand(score=7,value=(0+10))
                elif (stats["Queen"] >= 2):
                    players[index].modifyHand(score=7,value=(0+11))
                elif (stats["King"] >= 2):
                    players[index].modifyHand(score=7,value=(0+12))
                elif (stats["Ace"] >= 2):
                    players[index].modifyHand(score=7,value=(0+13))
            elif (stats["2"] == 3):
                if (stats["1"] >= 2):
                    players[index].modifyHand(score=7,value=(1+0))
                elif (stats["3"] >= 2):
                    players[index].modifyHand(score=7,value=(1+2))
                elif (stats["4"] >= 2):
                    players[index].modifyHand(score=7,value=(1+3))
                elif (stats["5"] >= 2):
                    players[index].modifyHand(score=7,value=(1+4))
                elif (stats["6"] >= 2):
                    players[index].modifyHand(score=7,value=(1+5))
                elif (stats["7"] >= 2):
                    players[index].modifyHand(score=7,value=(1+6))
                elif (stats["8"] >= 2):
                    players[index].modifyHand(score=7,value=(1+7))
                elif (stats["9"] >= 2):
                    players[index].modifyHand(score=7,value=(1+8))
                elif (stats["10"] >= 2):
                    players[index].modifyHand(score=7,value=(1+9))
                elif (stats["Jack"] >= 2):
                    players[index].modifyHand(score=7,value=(1+10))
                elif (stats["Queen"] >= 2):
                    players[index].modifyHand(score=7,value=(1+11))
                elif (stats["King"] >= 2):
                    players[index].modifyHand(score=7,value=(1+12))
                elif (stats["Ace"] >= 2):
                    players[index].modifyHand(score=7,value=(1+13))
            elif (stats["3"] == 3):
                if (stats["1"] >= 2):
                    players[index].modifyHand(score=7,value=(2+0))
                elif (stats["2"] >= 2):
                    players[index].modifyHand(score=7,value=(2+1))
                elif (stats["4"] >= 2):
                    players[index].modifyHand(score=7,value=(2+3))
                elif (stats["5"] >= 2):
                    players[index].modifyHand(score=7,value=(2+4))
                elif (stats["6"] >= 2):
                    players[index].modifyHand(score=7,value=(2+5))
                elif (stats["7"] >= 2):
                    players[index].modifyHand(score=7,value=(2+6))
                elif (stats["8"] >= 2):
                    players[index].modifyHand(score=7,value=(2+7))
                elif (stats["9"] >= 2):
                    players[index].modifyHand(score=7,value=(2+8))
                elif (stats["10"] >= 2):
                    players[index].modifyHand(score=7,value=(2+9))
                elif (stats["Jack"] >= 2):
                    players[index].modifyHand(score=7,value=(2+10))
                elif (stats["Queen"] >= 2):
                    players[index].modifyHand(score=7,value=(2+11))
                elif (stats["King"] >= 2):
                    players[index].modifyHand(score=7,value=(2+12))
                elif (stats["Ace"] >= 2):
                    players[index].modifyHand(score=7,value=(2+13))
            elif (stats["4"] == 3):
                if (stats["1"] >= 2):
                    players[index].modifyHand(score=7,value=(3+0))
                elif (stats["2"] >= 2):
                    players[index].modifyHand(score=7,value=(3+1))
                elif (stats["3"] >= 2):
                    players[index].modifyHand(score=7,value=(3+2))
                elif (stats["5"] >= 2):
                    players[index].modifyHand(score=7,value=(3+4))
                elif (stats["6"] >= 2):
                    players[index].modifyHand(score=7,value=(3+5))
                elif (stats["7"] >= 2):
                    players[index].modifyHand(score=7,value=(3+6))
                elif (stats["8"] >= 2):
                    players[index].modifyHand(score=7,value=(3+7))
                elif (stats["9"] >= 2):
                    players[index].modifyHand(score=7,value=(3+8))
                elif (stats["10"] >= 2):
                    players[index].modifyHand(score=7,value=(3+9))
                elif (stats["Jack"] >= 2):
                    players[index].modifyHand(score=7,value=(3+10))
                elif (stats["Queen"] >= 2):
                    players[index].modifyHand(score=7,value=(3+11))
                elif (stats["King"] >= 2):
                    players[index].modifyHand(score=7,value=(3+12))
                elif (stats["Ace"] >= 2):
                    players[index].modifyHand(score=7,value=(3+13))
            elif (stats["5"] == 3):
                if (stats["1"] >= 2):
                    players[index].modifyHand(score=7,value=(4+0))
                elif (stats["2"] >= 2):
                    players[index].modifyHand(score=7,value=(4+1))
                elif (stats["3"] >= 2):
                    players[index].modifyHand(score=7,value=(4+2))
                elif (stats["4"] >= 2):
                    players[index].modifyHand(score=7,value=(4+3))
                elif (stats["6"] >= 2):
                    players[index].modifyHand(score=7,value=(4+5))
                elif (stats["7"] >= 2):
                    players[index].modifyHand(score=7,value=(4+6))
                elif (stats["8"] >= 2):
                    players[index].modifyHand(score=7,value=(4+7))
                elif (stats["9"] >= 2):
                    players[index].modifyHand(score=7,value=(4+8))
                elif (stats["10"] >= 2):
                    players[index].modifyHand(score=7,value=(4+9))
                elif (stats["Jack"] >= 2):
                    players[index].modifyHand(score=7,value=(4+10))
                elif (stats["Queen"] >= 2):
                    players[index].modifyHand(score=7,value=(4+11))
                elif (stats["King"] >= 2):
                    players[index].modifyHand(score=7,value=(4+12))
                elif (stats["Ace"] >= 2):
                    players[index].modifyHand(score=7,value=(4+13))
            elif (stats["6"] == 3):
                if (stats["1"] >= 2):
                    players[index].modifyHand(score=7,value=(5+0))
                elif (stats["2"] >= 2):
                    players[index].modifyHand(score=7,value=(5+1))
                elif (stats["3"] >= 2):
                    players[index].modifyHand(score=7,value=(5+2))
                elif (stats["4"] >= 2):
                    players[index].modifyHand(score=7,value=(5+3))
                elif (stats["5"] >= 2):
                    players[index].modifyHand(score=7,value=(5+4))
                elif (stats["7"] >= 2):
                    players[index].modifyHand(score=7,value=(5+6))
                elif (stats["8"] >= 2):
                    players[index].modifyHand(score=7,value=(5+7))
                elif (stats["9"] >= 2):
                    players[index].modifyHand(score=7,value=(5+8))
                elif (stats["10"] >= 2):
                    players[index].modifyHand(score=7,value=(5+9))
                elif (stats["Jack"] >= 2):
                    players[index].modifyHand(score=7,value=(5+10))
                elif (stats["Queen"] >= 2):
                    players[index].modifyHand(score=7,value=(5+11))
                elif (stats["King"] >= 2):
                    players[index].modifyHand(score=7,value=(5+12))
                elif (stats["Ace"] >= 2):
                    players[index].modifyHand(score=7,value=(5+13))
            elif (stats["7"] == 3):
                if (stats["1"] >= 2):
                    players[index].modifyHand(score=7,value=(6+0))
                elif (stats["2"] >= 2):
                    players[index].modifyHand(score=7,value=(6+1))
                elif (stats["3"] >= 2):
                    players[index].modifyHand(score=7,value=(6+2))
                elif (stats["4"] >= 2):
                    players[index].modifyHand(score=7,value=(6+3))
                elif (stats["5"] >= 2):
                    players[index].modifyHand(score=7,value=(6+4))
                elif (stats["6"] >= 2):
                    players[index].modifyHand(score=7,value=(6+5))
                elif (stats["8"] >= 2):
                    players[index].modifyHand(score=7,value=(6+7))
                elif (stats["9"] >= 2):
                    players[index].modifyHand(score=7,value=(6+8))
                elif (stats["10"] >= 2):
                    players[index].modifyHand(score=7,value=(6+9))
                elif (stats["Jack"] >= 2):
                    players[index].modifyHand(score=7,value=(6+10))
                elif (stats["Queen"] >= 2):
                    players[index].modifyHand(score=7,value=(6+11))
                elif (stats["King"] >= 2):
                    players[index].modifyHand(score=7,value=(6+12))
                elif (stats["Ace"] >= 2):
                    players[index].modifyHand(score=7,value=(6+13))
            elif (stats["8"] == 3):
                if (stats["1"] >= 2):
                    players[index].modifyHand(score=7,value=(7+0))
                elif (stats["2"] >= 2):
                    players[index].modifyHand(score=7,value=(7+1))
                elif (stats["3"] >= 2):
                    players[index].modifyHand(score=7,value=(7+2))
                elif (stats["4"] >= 2):
                    players[index].modifyHand(score=7,value=(7+3))
                elif (stats["5"] >= 2):
                    players[index].modifyHand(score=7,value=(7+4))
                elif (stats["6"] >= 2):
                    players[index].modifyHand(score=7,value=(7+5))
                elif (stats["7"] >= 2):
                    players[index].modifyHand(score=7,value=(7+6))
                elif (stats["9"] >= 2):
                    players[index].modifyHand(score=7,value=(7+8))
                elif (stats["10"] >= 2):
                    players[index].modifyHand(score=7,value=(7+9))
                elif (stats["Jack"] >= 2):
                    players[index].modifyHand(score=7,value=(7+10))
                elif (stats["Queen"] >= 2):
                    players[index].modifyHand(score=7,value=(7+11))
                elif (stats["King"] >= 2):
                    players[index].modifyHand(score=7,value=(7+12))
                elif (stats["Ace"] >= 2):
                    players[index].modifyHand(score=7,value=(7+13))
            elif (stats["9"] == 3):
                if (stats["1"] >= 2):
                    players[index].modifyHand(score=7,value=(8+0))
                elif (stats["2"] >= 2):
                    players[index].modifyHand(score=7,value=(8+1))
                elif (stats["3"] >= 2):
                    players[index].modifyHand(score=7,value=(8+2))
                elif (stats["4"] >= 2):
                    players[index].modifyHand(score=7,value=(8+3))
                elif (stats["5"] >= 2):
                    players[index].modifyHand(score=7,value=(8+4))
                elif (stats["6"] >= 2):
                    players[index].modifyHand(score=7,value=(8+5))
                elif (stats["7"] >= 2):
                    players[index].modifyHand(score=7,value=(8+6))
                elif (stats["8"] >= 2):
                    players[index].modifyHand(score=7,value=(8+7))
                elif (stats["10"] >= 2):
                    players[index].modifyHand(score=7,value=(8+9))
                elif (stats["Jack"] >= 2):
                    players[index].modifyHand(score=7,value=(8+10))
                elif (stats["Queen"] >= 2):
                    players[index].modifyHand(score=7,value=(8+11))
                elif (stats["King"] >= 2):
                    players[index].modifyHand(score=7,value=(8+12))
                elif (stats["Ace"] >= 2):
                    players[index].modifyHand(score=7,value=(8+13))
            elif (stats["10"] == 3):
                if (stats["1"] >= 2):
                    players[index].modifyHand(score=7,value=(9+0))
                elif (stats["2"] >= 2):
                    players[index].modifyHand(score=7,value=(9+1))
                elif (stats["3"] >= 2):
                    players[index].modifyHand(score=7,value=(9+2))
                elif (stats["4"] >= 2):
                    players[index].modifyHand(score=7,value=(9+3))
                elif (stats["5"] >= 2):
                    players[index].modifyHand(score=7,value=(9+4))
                elif (stats["6"] >= 2):
                    players[index].modifyHand(score=7,value=(9+5))
                elif (stats["7"] >= 2):
                    players[index].modifyHand(score=7,value=(9+6))
                elif (stats["8"] >= 2):
                    players[index].modifyHand(score=7,value=(9+7))
                elif (stats["9"] >= 2):
                    players[index].modifyHand(score=7,value=(9+8))
                elif (stats["Jack"] >= 2):
                    players[index].modifyHand(score=7,value=(9+10))
                elif (stats["Queen"] >= 2):
                    players[index].modifyHand(score=7,value=(9+11))
                elif (stats["King"] >= 2):
                    players[index].modifyHand(score=7,value=(9+12))
                elif (stats["Ace"] >= 2):
                    players[index].modifyHand(score=7,value=(9+13))
            elif (stats["Jack"] == 3):
                if (stats["1"] >= 2):
                    players[index].modifyHand(score=7,value=(10+0))
                elif (stats["2"] >= 2):
                    players[index].modifyHand(score=7,value=(10+1))
                elif (stats["3"] >= 2):
                    players[index].modifyHand(score=7,value=(10+2))
                elif (stats["4"] >= 2):
                    players[index].modifyHand(score=7,value=(10+3))
                elif (stats["5"] >= 2):
                    players[index].modifyHand(score=7,value=(10+4))
                elif (stats["6"] >= 2):
                    players[index].modifyHand(score=7,value=(10+5))
                elif (stats["7"] >= 2):
                    players[index].modifyHand(score=7,value=(10+6))
                elif (stats["8"] >= 2):
                    players[index].modifyHand(score=7,value=(10+7))
                elif (stats["9"] >= 2):
                    players[index].modifyHand(score=7,value=(10+8))
                elif (stats["10"] >= 2):
                    players[index].modifyHand(score=7,value=(10+9))
                elif (stats["Queen"] >= 2):
                    players[index].modifyHand(score=7,value=(10+11))
                elif (stats["King"] >= 2):
                    players[index].modifyHand(score=7,value=(10+12))
                elif (stats["Ace"] >= 2):
                    players[index].modifyHand(score=7,value=(10+13))
            elif (stats["Queen"] == 3):
                if (stats["1"] >= 2):
                    players[index].modifyHand(score=7,value=(11+0))
                elif (stats["2"] >= 2):
                    players[index].modifyHand(score=7,value=(11+1))
                elif (stats["3"] >= 2):
                    players[index].modifyHand(score=7,value=(11+2))
                elif (stats["4"] >= 2):
                    players[index].modifyHand(score=7,value=(11+3))
                elif (stats["5"] >= 2):
                    players[index].modifyHand(score=7,value=(11+4))
                elif (stats["6"] >= 2):
                    players[index].modifyHand(score=7,value=(11+5))
                elif (stats["7"] >= 2):
                    players[index].modifyHand(score=7,value=(11+6))
                elif (stats["8"] >= 2):
                    players[index].modifyHand(score=7,value=(11+7))
                elif (stats["9"] >= 2):
                    players[index].modifyHand(score=7,value=(11+8))
                elif (stats["10"] >= 2):
                    players[index].modifyHand(score=7,value=(11+9))
                elif (stats["Jack"] >= 2):
                    players[index].modifyHand(score=7,value=(11+10))
                elif (stats["King"] >= 2):
                    players[index].modifyHand(score=7,value=(11+12))
                elif (stats["Ace"] >= 2):
                    players[index].modifyHand(score=7,value=(11+13))
            elif (stats["King"] == 3):
                if (stats["1"] >= 2):
                    players[index].modifyHand(score=7,value=(12+0))
                elif (stats["2"] >= 2):
                    players[index].modifyHand(score=7,value=(12+1))
                elif (stats["3"] >= 2):
                    players[index].modifyHand(score=7,value=(12+2))
                elif (stats["4"] >= 2):
                    players[index].modifyHand(score=7,value=(12+3))
                elif (stats["5"] >= 2):
                    players[index].modifyHand(score=7,value=(12+4))
                elif (stats["6"] >= 2):
                    players[index].modifyHand(score=7,value=(12+5))
                elif (stats["7"] >= 2):
                    players[index].modifyHand(score=7,value=(12+6))
                elif (stats["8"] >= 2):
                    players[index].modifyHand(score=7,value=(12+7))
                elif (stats["9"] >= 2):
                    players[index].modifyHand(score=7,value=(12+8))
                elif (stats["10"] >= 2):
                    players[index].modifyHand(score=7,value=(12+9))
                elif (stats["Jack"] >= 2):
                    players[index].modifyHand(score=7,value=(12+10))
                elif (stats["Queen"] >= 2):
                    players[index].modifyHand(score=7,value=(12+11))
                elif (stats["Ace"] >= 2):
                    players[index].modifyHand(score=7,value=(12+13))
            elif (stats["Ace"] == 3):
                if (stats["1"] >= 2):
                    players[index].modifyHand(score=7,value=(13+0))
                elif (stats["2"] >= 2):
                    players[index].modifyHand(score=7,value=(13+1))
                elif (stats["3"] >= 2):
                    players[index].modifyHand(score=7,value=(13+2))
                elif (stats["4"] >= 2):
                    players[index].modifyHand(score=7,value=(13+3))
                elif (stats["5"] >= 2):
                    players[index].modifyHand(score=7,value=(13+4))
                elif (stats["6"] >= 2):
                    players[index].modifyHand(score=7,value=(13+5))
                elif (stats["7"] >= 2):
                    players[index].modifyHand(score=7,value=(13+6))
                elif (stats["8"] >= 2):
                    players[index].modifyHand(score=7,value=(13+7))
                elif (stats["9"] >= 2):
                    players[index].modifyHand(score=7,value=(13+8))
                elif (stats["10"] >= 2):
                    players[index].modifyHand(score=7,value=(13+9))
                elif (stats["Jack"] >= 2):
                    players[index].modifyHand(score=7,value=(13+10))
                elif (stats["Queen"] >= 2):
                    players[index].modifyHand(score=7,value=(13+11))
                elif (stats["King"] >= 2):
                    players[index].modifyHand(score=7,value=(13+12))
            elif (stats["1"] == 2):
                if (stats["2"] >= 3):
                    players[index].modifyHand(score=7,value=(0+1))
                elif (stats["3"] >= 3):
                    players[index].modifyHand(score=7,value=(0+2))
                elif (stats["4"] >= 3):
                    players[index].modifyHand(score=7,value=(0+3))
                elif (stats["5"] >= 3):
                    players[index].modifyHand(score=7,value=(0+4))
                elif (stats["6"] >= 3):
                    players[index].modifyHand(score=7,value=(0+5))
                elif (stats["7"] >= 3):
                    players[index].modifyHand(score=7,value=(0+6))
                elif (stats["8"] >= 3):
                    players[index].modifyHand(score=7,value=(0+7))
                elif (stats["9"] >= 3):
                    players[index].modifyHand(score=7,value=(0+8))
                elif (stats["10"] >= 3):
                    players[index].modifyHand(score=7,value=(0+9))
                elif (stats["Jack"] >= 3):
                    players[index].modifyHand(score=7,value=(0+10))
                elif (stats["Queen"] >= 3):
                    players[index].modifyHand(score=7,value=(0+11))
                elif (stats["King"] >= 3):
                    players[index].modifyHand(score=7,value=(0+12))
                elif (stats["Ace"] >= 3):
                    players[index].modifyHand(score=7,value=(0+13))
            elif (stats["2"] == 2):
                if (stats["1"] >= 3):
                    players[index].modifyHand(score=7,value=(1+0))
                elif (stats["3"] >= 3):
                    players[index].modifyHand(score=7,value=(1+2))
                elif (stats["4"] >= 3):
                    players[index].modifyHand(score=7,value=(1+3))
                elif (stats["5"] >= 3):
                    players[index].modifyHand(score=7,value=(1+4))
                elif (stats["6"] >= 3):
                    players[index].modifyHand(score=7,value=(1+5))
                elif (stats["7"] >= 3):
                    players[index].modifyHand(score=7,value=(1+6))
                elif (stats["8"] >= 3):
                    players[index].modifyHand(score=7,value=(1+7))
                elif (stats["9"] >= 3):
                    players[index].modifyHand(score=7,value=(1+8))
                elif (stats["10"] >= 3):
                    players[index].modifyHand(score=7,value=(1+9))
                elif (stats["Jack"] >= 3):
                    players[index].modifyHand(score=7,value=(1+10))
                elif (stats["Queen"] >= 3):
                    players[index].modifyHand(score=7,value=(1+11))
                elif (stats["King"] >= 3):
                    players[index].modifyHand(score=7,value=(1+12))
                elif (stats["Ace"] >= 3):
                    players[index].modifyHand(score=7,value=(1+13))
            elif (stats["3"] == 2):
                if (stats["1"] >= 3):
                    players[index].modifyHand(score=7,value=(2+0))
                elif (stats["2"] >= 3):
                    players[index].modifyHand(score=7,value=(2+1))
                elif (stats["4"] >= 3):
                    players[index].modifyHand(score=7,value=(2+3))
                elif (stats["5"] >= 3):
                    players[index].modifyHand(score=7,value=(2+4))
                elif (stats["6"] >= 3):
                    players[index].modifyHand(score=7,value=(2+5))
                elif (stats["7"] >= 3):
                    players[index].modifyHand(score=7,value=(2+6))
                elif (stats["8"] >= 3):
                    players[index].modifyHand(score=7,value=(2+7))
                elif (stats["9"] >= 3):
                    players[index].modifyHand(score=7,value=(2+8))
                elif (stats["10"] >= 3):
                    players[index].modifyHand(score=7,value=(2+9))
                elif (stats["Jack"] >= 3):
                    players[index].modifyHand(score=7,value=(2+10))
                elif (stats["Queen"] >= 3):
                    players[index].modifyHand(score=7,value=(2+11))
                elif (stats["King"] >= 3):
                    players[index].modifyHand(score=7,value=(2+12))
                elif (stats["Ace"] >= 3):
                    players[index].modifyHand(score=7,value=(2+13))
            elif (stats["4"] == 2):
                if (stats["1"] >= 3):
                    players[index].modifyHand(score=7,value=(3+0))
                elif (stats["2"] >= 3):
                    players[index].modifyHand(score=7,value=(3+1))
                elif (stats["3"] >= 3):
                    players[index].modifyHand(score=7,value=(3+2))
                elif (stats["5"] >= 3):
                    players[index].modifyHand(score=7,value=(3+4))
                elif (stats["6"] >= 3):
                    players[index].modifyHand(score=7,value=(3+5))
                elif (stats["7"] >= 3):
                    players[index].modifyHand(score=7,value=(3+6))
                elif (stats["8"] >= 3):
                    players[index].modifyHand(score=7,value=(3+7))
                elif (stats["9"] >= 3):
                    players[index].modifyHand(score=7,value=(3+8))
                elif (stats["10"] >= 3):
                    players[index].modifyHand(score=7,value=(3+9))
                elif (stats["Jack"] >= 3):
                    players[index].modifyHand(score=7,value=(3+10))
                elif (stats["Queen"] >= 3):
                    players[index].modifyHand(score=7,value=(3+11))
                elif (stats["King"] >= 3):
                    players[index].modifyHand(score=7,value=(3+12))
                elif (stats["Ace"] >= 3):
                    players[index].modifyHand(score=7,value=(3+13))
            elif (stats["5"] == 2):
                if (stats["1"] >= 3):
                    players[index].modifyHand(score=7,value=(4+0))
                elif (stats["2"] >= 3):
                    players[index].modifyHand(score=7,value=(4+1))
                elif (stats["3"] >= 3):
                    players[index].modifyHand(score=7,value=(4+2))
                elif (stats["4"] >= 3):
                    players[index].modifyHand(score=7,value=(4+3))
                elif (stats["6"] >= 3):
                    players[index].modifyHand(score=7,value=(4+5))
                elif (stats["7"] >= 3):
                    players[index].modifyHand(score=7,value=(4+6))
                elif (stats["8"] >= 3):
                    players[index].modifyHand(score=7,value=(4+7))
                elif (stats["9"] >= 3):
                    players[index].modifyHand(score=7,value=(4+8))
                elif (stats["10"] >= 3):
                    players[index].modifyHand(score=7,value=(4+9))
                elif (stats["Jack"] >= 3):
                    players[index].modifyHand(score=7,value=(4+10))
                elif (stats["Queen"] >= 3):
                    players[index].modifyHand(score=7,value=(4+11))
                elif (stats["King"] >= 3):
                    players[index].modifyHand(score=7,value=(4+12))
                elif (stats["Ace"] >= 3):
                    players[index].modifyHand(score=7,value=(4+13))
            elif (stats["6"] == 2):
                if (stats["1"] >= 3):
                    players[index].modifyHand(score=7,value=(5+0))
                elif (stats["2"] >= 3):
                    players[index].modifyHand(score=7,value=(5+1))
                elif (stats["3"] >= 3):
                    players[index].modifyHand(score=7,value=(5+2))
                elif (stats["4"] >= 3):
                    players[index].modifyHand(score=7,value=(5+3))
                elif (stats["5"] >= 3):
                    players[index].modifyHand(score=7,value=(5+4))
                elif (stats["7"] >= 3):
                    players[index].modifyHand(score=7,value=(5+6))
                elif (stats["8"] >= 3):
                    players[index].modifyHand(score=7,value=(5+7))
                elif (stats["9"] >= 3):
                    players[index].modifyHand(score=7,value=(5+8))
                elif (stats["10"] >= 3):
                    players[index].modifyHand(score=7,value=(5+9))
                elif (stats["Jack"] >= 3):
                    players[index].modifyHand(score=7,value=(5+10))
                elif (stats["Queen"] >= 3):
                    players[index].modifyHand(score=7,value=(5+11))
                elif (stats["King"] >= 3):
                    players[index].modifyHand(score=7,value=(5+12))
                elif (stats["Ace"] >= 3):
                    players[index].modifyHand(score=7,value=(5+13))
            elif (stats["7"] == 2):
                if (stats["1"] >= 3):
                    players[index].modifyHand(score=7,value=(6+0))
                elif (stats["2"] >= 3):
                    players[index].modifyHand(score=7,value=(6+1))
                elif (stats["3"] >= 3):
                    players[index].modifyHand(score=7,value=(6+2))
                elif (stats["4"] >= 3):
                    players[index].modifyHand(score=7,value=(6+3))
                elif (stats["5"] >= 3):
                    players[index].modifyHand(score=7,value=(6+4))
                elif (stats["6"] >= 3):
                    players[index].modifyHand(score=7,value=(6+5))
                elif (stats["8"] >= 3):
                    players[index].modifyHand(score=7,value=(6+7))
                elif (stats["9"] >= 3):
                    players[index].modifyHand(score=7,value=(6+8))
                elif (stats["10"] >= 3):
                    players[index].modifyHand(score=7,value=(6+9))
                elif (stats["Jack"] >= 3):
                    players[index].modifyHand(score=7,value=(6+10))
                elif (stats["Queen"] >= 3):
                    players[index].modifyHand(score=7,value=(6+11))
                elif (stats["King"] >= 3):
                    players[index].modifyHand(score=7,value=(6+12))
                elif (stats["Ace"] >= 3):
                    players[index].modifyHand(score=7,value=(6+13))
            elif (stats["8"] == 2):
                if (stats["1"] >= 3):
                    players[index].modifyHand(score=7,value=(7+0))
                elif (stats["2"] >= 3):
                    players[index].modifyHand(score=7,value=(7+1))
                elif (stats["3"] >= 3):
                    players[index].modifyHand(score=7,value=(7+2))
                elif (stats["4"] >= 3):
                    players[index].modifyHand(score=7,value=(7+3))
                elif (stats["5"] >= 3):
                    players[index].modifyHand(score=7,value=(7+4))
                elif (stats["6"] >= 3):
                    players[index].modifyHand(score=7,value=(7+5))
                elif (stats["7"] >= 3):
                    players[index].modifyHand(score=7,value=(7+6))
                elif (stats["9"] >= 3):
                    players[index].modifyHand(score=7,value=(7+8))
                elif (stats["10"] >= 3):
                    players[index].modifyHand(score=7,value=(7+9))
                elif (stats["Jack"] >= 3):
                    players[index].modifyHand(score=7,value=(7+10))
                elif (stats["Queen"] >= 3):
                    players[index].modifyHand(score=7,value=(7+11))
                elif (stats["King"] >= 3):
                    players[index].modifyHand(score=7,value=(7+12))
                elif (stats["Ace"] >= 3):
                    players[index].modifyHand(score=7,value=(7+13))
            elif (stats["9"] == 2):
                if (stats["1"] >= 3):
                    players[index].modifyHand(score=7,value=(8+0))
                elif (stats["2"] >= 3):
                    players[index].modifyHand(score=7,value=(8+1))
                elif (stats["3"] >= 3):
                    players[index].modifyHand(score=7,value=(8+2))
                elif (stats["4"] >= 3):
                    players[index].modifyHand(score=7,value=(8+3))
                elif (stats["5"] >= 3):
                    players[index].modifyHand(score=7,value=(8+4))
                elif (stats["6"] >= 3):
                    players[index].modifyHand(score=7,value=(8+5))
                elif (stats["7"] >= 3):
                    players[index].modifyHand(score=7,value=(8+6))
                elif (stats["8"] >= 3):
                    players[index].modifyHand(score=7,value=(8+7))
                elif (stats["10"] >= 3):
                    players[index].modifyHand(score=7,value=(8+9))
                elif (stats["Jack"] >= 3):
                    players[index].modifyHand(score=7,value=(8+10))
                elif (stats["Queen"] >= 3):
                    players[index].modifyHand(score=7,value=(8+11))
                elif (stats["King"] >= 3):
                    players[index].modifyHand(score=7,value=(8+12))
                elif (stats["Ace"] >= 3):
                    players[index].modifyHand(score=7,value=(8+13))
            elif (stats["10"] == 2):
                if (stats["1"] >= 3):
                    players[index].modifyHand(score=7,value=(9+0))
                elif (stats["2"] >= 3):
                    players[index].modifyHand(score=7,value=(9+1))
                elif (stats["3"] >= 3):
                    players[index].modifyHand(score=7,value=(9+2))
                elif (stats["4"] >= 3):
                    players[index].modifyHand(score=7,value=(9+3))
                elif (stats["5"] >= 3):
                    players[index].modifyHand(score=7,value=(9+4))
                elif (stats["6"] >= 3):
                    players[index].modifyHand(score=7,value=(9+5))
                elif (stats["7"] >= 3):
                    players[index].modifyHand(score=7,value=(9+6))
                elif (stats["8"] >= 3):
                    players[index].modifyHand(score=7,value=(9+7))
                elif (stats["9"] >= 3):
                    players[index].modifyHand(score=7,value=(9+8))
                elif (stats["Jack"] >= 3):
                    players[index].modifyHand(score=7,value=(9+10))
                elif (stats["Queen"] >= 3):
                    players[index].modifyHand(score=7,value=(9+11))
                elif (stats["King"] >= 3):
                    players[index].modifyHand(score=7,value=(9+12))
                elif (stats["Ace"] >= 3):
                    players[index].modifyHand(score=7,value=(9+13))
            elif (stats["Jack"] == 2):
                if (stats["1"] >= 3):
                    players[index].modifyHand(score=7,value=(10+0))
                elif (stats["2"] >= 3):
                    players[index].modifyHand(score=7,value=(10+1))
                elif (stats["3"] >= 3):
                    players[index].modifyHand(score=7,value=(10+2))
                elif (stats["4"] >= 3):
                    players[index].modifyHand(score=7,value=(10+3))
                elif (stats["5"] >= 3):
                    players[index].modifyHand(score=7,value=(10+4))
                elif (stats["6"] >= 3):
                    players[index].modifyHand(score=7,value=(10+5))
                elif (stats["7"] >= 3):
                    players[index].modifyHand(score=7,value=(10+6))
                elif (stats["8"] >= 3):
                    players[index].modifyHand(score=7,value=(10+7))
                elif (stats["9"] >= 3):
                    players[index].modifyHand(score=7,value=(10+8))
                elif (stats["10"] >= 3):
                    players[index].modifyHand(score=7,value=(10+9))
                elif (stats["Queen"] >= 3):
                    players[index].modifyHand(score=7,value=(10+11))
                elif (stats["King"] >= 3):
                    players[index].modifyHand(score=7,value=(10+12))
                elif (stats["Ace"] >= 3):
                    players[index].modifyHand(score=7,value=(10+13))
            elif (stats["Queen"] == 2):
                if (stats["1"] >= 3):
                    players[index].modifyHand(score=7,value=(11+0))
                elif (stats["2"] >= 3):
                    players[index].modifyHand(score=7,value=(11+1))
                elif (stats["3"] >= 3):
                    players[index].modifyHand(score=7,value=(11+2))
                elif (stats["4"] >= 3):
                    players[index].modifyHand(score=7,value=(11+3))
                elif (stats["5"] >= 3):
                    players[index].modifyHand(score=7,value=(11+4))
                elif (stats["6"] >= 3):
                    players[index].modifyHand(score=7,value=(11+5))
                elif (stats["7"] >= 3):
                    players[index].modifyHand(score=7,value=(11+6))
                elif (stats["8"] >= 3):
                    players[index].modifyHand(score=7,value=(11+7))
                elif (stats["9"] >= 3):
                    players[index].modifyHand(score=7,value=(11+8))
                elif (stats["10"] >= 3):
                    players[index].modifyHand(score=7,value=(11+9))
                elif (stats["Jack"] >= 3):
                    players[index].modifyHand(score=7,value=(11+10))
                elif (stats["King"] >= 3):
                    players[index].modifyHand(score=7,value=(11+12))
                elif (stats["Ace"] >= 3):
                    players[index].modifyHand(score=7,value=(11+13))
            elif (stats["King"] == 2):
                if (stats["1"] >= 3):
                    players[index].modifyHand(score=7,value=(12+0))
                elif (stats["2"] >= 3):
                    players[index].modifyHand(score=7,value=(12+1))
                elif (stats["3"] >= 3):
                    players[index].modifyHand(score=7,value=(12+2))
                elif (stats["4"] >= 3):
                    players[index].modifyHand(score=7,value=(12+3))
                elif (stats["5"] >= 3):
                    players[index].modifyHand(score=7,value=(12+4))
                elif (stats["6"] >= 3):
                    players[index].modifyHand(score=7,value=(12+5))
                elif (stats["7"] >= 3):
                    players[index].modifyHand(score=7,value=(12+6))
                elif (stats["8"] >= 3):
                    players[index].modifyHand(score=7,value=(12+7))
                elif (stats["9"] >= 3):
                    players[index].modifyHand(score=7,value=(12+8))
                elif (stats["10"] >= 3):
                    players[index].modifyHand(score=7,value=(12+9))
                elif (stats["Jack"] >= 3):
                    players[index].modifyHand(score=7,value=(12+10))
                elif (stats["Queen"] >= 3):
                    players[index].modifyHand(score=7,value=(12+11))
                elif (stats["Ace"] >= 3):
                    players[index].modifyHand(score=7,value=(12+13))
            elif (stats["Ace"] == 2):
                if (stats["1"] >= 3):
                    players[index].modifyHand(score=7,value=(13+0))
                elif (stats["2"] >= 3):
                    players[index].modifyHand(score=7,value=(13+1))
                elif (stats["3"] >= 3):
                    players[index].modifyHand(score=7,value=(13+2))
                elif (stats["4"] >= 3):
                    players[index].modifyHand(score=7,value=(13+3))
                elif (stats["5"] >= 3):
                    players[index].modifyHand(score=7,value=(13+4))
                elif (stats["6"] >= 3):
                    players[index].modifyHand(score=7,value=(13+5))
                elif (stats["7"] >= 3):
                    players[index].modifyHand(score=7,value=(13+6))
                elif (stats["8"] >= 3):
                    players[index].modifyHand(score=7,value=(13+7))
                elif (stats["9"] >= 3):
                    players[index].modifyHand(score=7,value=(13+8))
                elif (stats["10"] >= 3):
                    players[index].modifyHand(score=7,value=(13+9))
                elif (stats["Jack"] >= 3):
                    players[index].modifyHand(score=7,value=(13+10))
                elif (stats["Queen"] >= 3):
                    players[index].modifyHand(score=7,value=(13+11))
                elif (stats["King"] >= 3):
                    players[index].modifyHand(score=7,value=(13+12))

            # 6  - checking for a flush (five of the same suit) - this should be the result given
            if (stats["d"] >= 5) or (stats["c"] >= 5) or (stats["h"] >= 5) or (stats["s"] >= 5):
                players[index].modifyHandValue(score=6)
            
            # 5  - checking for a straight (five cards in rank order)
            if (stats["Ace"] >= 1) and  (stats["1"] >= 1) and (stats["2"] >= 1) and  (stats["3"] >= 1) and (stats["4"] >= 1):
                players[index].modifyHandValue(score=5,value=0)
            elif (stats["1"] >= 1) and  (stats["2"] >= 1) and (stats["3"] >= 1) and  (stats["4"] >= 1) and (stats["5"] >= 1):
                players[index].modifyHandValue(score=5,value=1)
            elif (stats["2"] >= 1) and  (stats["3"] >= 1) and (stats["4"] >= 1) and  (stats["5"] >= 1) and (stats["6"] >= 1):
                players[index].modifyHandValue(score=5,value=2)
            elif (stats["3"] >= 1) and  (stats["4"] >= 1) and (stats["5"] >= 1) and  (stats["6"] >= 1) and (stats["7"] >= 1):
                players[index].modifyHandValue(score=5,value=3)
            elif (stats["4"] >= 1) and  (stats["5"] >= 1) and (stats["6"] >= 1) and  (stats["7"] >= 1) and (stats["8"] >= 1):
                players[index].modifyHandValue(score=5,value=4)
            elif (stats["5"] >= 1) and  (stats["6"] >= 1) and (stats["7"] >= 1) and  (stats["8"] >= 1) and (stats["9"] >= 1):
                players[index].modifyHandValue(score=5,value=5)
            elif (stats["6"] >= 1) and  (stats["7"] >= 1) and (stats["8"] >= 1) and  (stats["9"] >= 1) and (stats["10"] >= 1):
                players[index].modifyHandValue(score=5,value=6)
            elif (stats["7"] >= 1) and  (stats["8"] >= 1) and (stats["9"] >= 1) and  (stats["10"] >= 1) and (stats["Jack"] >= 1):
                players[index].modifyHandValue(score=5,value=7)
            elif (stats["8"] >= 1) and  (stats["9"] >= 1) and (stats["10"] >= 1) and  (stats["Jack"] >= 1) and (stats["King"] >= 1):
                players[index].modifyHandValue(score=5,value=8)
            elif (stats["9"] >= 1) and  (stats["10"] >= 1) and (stats["Jack"] >= 1) and  (stats["Queen"] >= 1) and (stats["Queen"] >= 1):
                players[index].modifyHandValue(score=5,value=9)
            elif (stats["10"] >= 1) and  (stats["Jack"] >= 1) and (stats["Queen"] >= 1) and  (stats["King"] >= 1) and (stats["Ace"] >= 1):
                players[index].modifyHandValue(score=5,value=10)
            
            # 4  - checking for three of a kind
            if (stats["1"] == 3) or (stats["2"] == 3) or (stats["3"] == 3) or (stats["4"] == 3) or (stats["5"] == 3) or (stats["6"] == 3) or (stats["7"] == 3) or (stats["8"] == 3) or (stats["9"] == 3) or (stats["10"] == 3) or (stats["Jack"] == 3) or (stats["Queen"] == 3) or (stats["King"] == 3) or (stats["Ace"] == 3):
                players[index].modifyHandValue(score=4)
            
            # 3  - checking for two pair
            if (stats["1"] == 2):
                if (stats["2"] == 2):
                    players[index].modifyHandValue(score=3,value=(0+1))
                elif (stats["3"] == 2):
                    players[index].modifyHandValue(score=3,value=(0+2))
                elif (stats["4"] == 2):
                    players[index].modifyHandValue(score=3,value=(0+3))
                elif (stats["5"] == 2):
                    players[index].modifyHandValue(score=3,value=(0+4))
                elif (stats["6"] == 2):
                    players[index].modifyHandValue(score=3,value=(0+5))
                elif (stats["7"] == 2):
                    players[index].modifyHandValue(score=3,value=(0+6))
                elif (stats["8"] == 2):
                    players[index].modifyHandValue(score=3,value=(0+7))
                elif (stats["9"] == 2):
                    players[index].modifyHandValue(score=3,value=(0+8))
                elif (stats["10"] == 2):
                    players[index].modifyHandValue(score=3,value=(0+9))
                elif (stats["Jack"] == 2):
                    players[index].modifyHandValue(score=3,value=(0+10))
                elif (stats["Queen"] == 2):
                    players[index].modifyHandValue(score=3,value=(0+11))
                elif (stats["King"] == 2):
                    players[index].modifyHandValue(score=3,value=(0+12))
                elif (stats["Ace"] == 2):
                    players[index].modifyHandValue(score=3,value=(0+13))
            elif (stats["2"] == 2):
                if (stats["1"] == 2):
                    players[index].modifyHandValue(score=3,value=(1+0))
                elif (stats["3"] == 2):
                    players[index].modifyHandValue(score=3,value=(1+2))
                elif (stats["4"] == 2):
                    players[index].modifyHandValue(score=3,value=(1+3))
                elif (stats["5"] == 2):
                    players[index].modifyHandValue(score=3,value=(1+4))
                elif (stats["6"] == 2):
                    players[index].modifyHandValue(score=3,value=(1+5))
                elif (stats["7"] == 2):
                    players[index].modifyHandValue(score=3,value=(1+6))
                elif (stats["8"] == 2):
                    players[index].modifyHandValue(score=3,value=(1+7))
                elif (stats["9"] == 2):
                    players[index].modifyHandValue(score=3,value=(1+8))
                elif (stats["10"] == 2):
                    players[index].modifyHandValue(score=3,value=(1+9))
                elif (stats["Jack"] == 2):
                    players[index].modifyHandValue(score=3,value=(1+10))
                elif (stats["Queen"] == 2):
                    players[index].modifyHandValue(score=3,value=(1+11))
                elif (stats["King"] == 2):
                    players[index].modifyHandValue(score=3,value=(1+12))
                elif (stats["Ace"] == 2):
                    players[index].modifyHandValue(score=3,value=(1+13))
            elif (stats["3"] == 2):
                if (stats["1"] == 2):
                    players[index].modifyHandValue(score=3,value=(2+0))
                elif (stats["2"] == 2):
                    players[index].modifyHandValue(score=3,value=(2+1))
                elif (stats["4"] == 2):
                    players[index].modifyHandValue(score=3,value=(2+3))
                elif (stats["5"] == 2):
                    players[index].modifyHandValue(score=3,value=(2+4))
                elif (stats["6"] == 2):
                    players[index].modifyHandValue(score=3,value=(2+5))
                elif (stats["7"] == 2):
                    players[index].modifyHandValue(score=3,value=(2+6))
                elif (stats["8"] == 2):
                    players[index].modifyHandValue(score=3,value=(2+7))
                elif (stats["9"] == 2):
                    players[index].modifyHandValue(score=3,value=(2+8))
                elif (stats["10"] == 2):
                    players[index].modifyHandValue(score=3,value=(2+9))
                elif (stats["Jack"] == 2):
                    players[index].modifyHandValue(score=3,value=(2+10))
                elif (stats["Queen"] == 2):
                    players[index].modifyHandValue(score=3,value=(2+11))
                elif (stats["King"] == 2):
                    players[index].modifyHandValue(score=3,value=(2+12))
                elif (stats["Ace"] == 2):
                    players[index].modifyHandValue(score=3,value=(2+13))
            elif (stats["4"] == 2):
                if (stats["1"] == 2):
                    players[index].modifyHandValue(score=3,value=(3+0))
                elif (stats["2"] == 2):
                    players[index].modifyHandValue(score=3,value=(3+1))
                elif (stats["3"] == 2):
                    players[index].modifyHandValue(score=3,value=(3+2))
                elif (stats["5"] == 2):
                    players[index].modifyHandValue(score=3,value=(3+4))
                elif (stats["6"] == 2):
                    players[index].modifyHandValue(score=3,value=(3+5))
                elif (stats["7"] == 2):
                    players[index].modifyHandValue(score=3,value=(3+6))
                elif (stats["8"] == 2):
                    players[index].modifyHandValue(score=3,value=(3+7))
                elif (stats["9"] == 2):
                    players[index].modifyHandValue(score=3,value=(3+8))
                elif (stats["10"] == 2):
                    players[index].modifyHandValue(score=3,value=(3+9))
                elif (stats["Jack"] == 2):
                    players[index].modifyHandValue(score=3,value=(3+10))
                elif (stats["Queen"] == 2):
                    players[index].modifyHandValue(score=3,value=(3+11))
                elif (stats["King"] == 2):
                    players[index].modifyHandValue(score=3,value=(3+12))
                elif (stats["Ace"] == 2):
                    players[index].modifyHandValue(score=3,value=(3+13))
            elif (stats["5"] == 2):
                if (stats["1"] == 2):
                    players[index].modifyHandValue(score=3,value=(4+0))
                elif (stats["2"] == 2):
                    players[index].modifyHandValue(score=3,value=(4+1))
                elif (stats["3"] == 2):
                    players[index].modifyHandValue(score=3,value=(4+2))
                elif (stats["4"] == 2):
                    players[index].modifyHandValue(score=3,value=(4+3))
                elif (stats["6"] == 2):
                    players[index].modifyHandValue(score=3,value=(4+5))
                elif (stats["7"] == 2):
                    players[index].modifyHandValue(score=3,value=(4+6))
                elif (stats["8"] == 2):
                    players[index].modifyHandValue(score=3,value=(4+7))
                elif (stats["9"] == 2):
                    players[index].modifyHandValue(score=3,value=(4+8))
                elif (stats["10"] == 2):
                    players[index].modifyHandValue(score=3,value=(4+9))
                elif (stats["Jack"] == 2):
                    players[index].modifyHandValue(score=3,value=(4+10))
                elif (stats["Queen"] == 2):
                    players[index].modifyHandValue(score=3,value=(4+11))
                elif (stats["King"] == 2):
                    players[index].modifyHandValue(score=3,value=(4+12))
                elif (stats["Ace"] == 2):
                    players[index].modifyHandValue(score=3,value=(4+13))
            elif (stats["6"] == 2):
                if (stats["1"] == 2):
                    players[index].modifyHandValue(score=3,value=(5+0))
                elif (stats["2"] == 2):
                    players[index].modifyHandValue(score=3,value=(5+1))
                elif (stats["3"] == 2):
                    players[index].modifyHandValue(score=3,value=(5+2))
                elif (stats["4"] == 2):
                    players[index].modifyHandValue(score=3,value=(5+3))
                elif (stats["5"] == 2):
                    players[index].modifyHandValue(score=3,value=(5+4))
                elif (stats["7"] == 2):
                    players[index].modifyHandValue(score=3,value=(5+6))
                elif (stats["8"] == 2):
                    players[index].modifyHandValue(score=3,value=(5+7))
                elif (stats["9"] == 2):
                    players[index].modifyHandValue(score=3,value=(5+8))
                elif (stats["10"] == 2):
                    players[index].modifyHandValue(score=3,value=(5+9))
                elif (stats["Jack"] == 2):
                    players[index].modifyHandValue(score=3,value=(5+10))
                elif (stats["Queen"] == 2):
                    players[index].modifyHandValue(score=3,value=(5+11))
                elif (stats["King"] == 2):
                    players[index].modifyHandValue(score=3,value=(5+12))
                elif (stats["Ace"] == 2):
                    players[index].modifyHandValue(score=3,value=(5+13))
            elif (stats["7"] == 2):
                if (stats["1"] == 2):
                    players[index].modifyHandValue(score=3,value=(6+0))
                elif (stats["2"] == 2):
                    players[index].modifyHandValue(score=3,value=(6+1))
                elif (stats["3"] == 2):
                    players[index].modifyHandValue(score=3,value=(6+2))
                elif (stats["4"] == 2):
                    players[index].modifyHandValue(score=3,value=(6+3))
                elif (stats["5"] == 2):
                    players[index].modifyHandValue(score=3,value=(6+4))
                elif (stats["6"] == 2):
                    players[index].modifyHandValue(score=3,value=(6+5))
                elif (stats["8"] == 2):
                    players[index].modifyHandValue(score=3,value=(6+7))
                elif (stats["9"] == 2):
                    players[index].modifyHandValue(score=3,value=(6+8))
                elif (stats["10"] == 2):
                    players[index].modifyHandValue(score=3,value=(6+9))
                elif (stats["Jack"] == 2):
                    players[index].modifyHandValue(score=3,value=(6+10))
                elif (stats["Queen"] == 2):
                    players[index].modifyHandValue(score=3,value=(6+11))
                elif (stats["King"] == 2):
                    players[index].modifyHandValue(score=3,value=(6+12))
                elif (stats["Ace"] == 2):
                    players[index].modifyHandValue(score=3,value=(6+13))
            elif (stats["8"] == 2):
                if (stats["1"] == 2):
                    players[index].modifyHandValue(score=3,value=(7+0))
                elif (stats["2"] == 2):
                    players[index].modifyHandValue(score=3,value=(7+1))
                elif (stats["3"] == 2):
                    players[index].modifyHandValue(score=3,value=(7+2))
                elif (stats["4"] == 2):
                    players[index].modifyHandValue(score=3,value=(7+3))
                elif (stats["5"] == 2):
                    players[index].modifyHandValue(score=3,value=(7+4))
                elif (stats["6"] == 2):
                    players[index].modifyHandValue(score=3,value=(7+5))
                elif (stats["7"] == 2):
                    players[index].modifyHandValue(score=3,value=(7+6))
                elif (stats["9"] == 2):
                    players[index].modifyHandValue(score=3,value=(7+8))
                elif (stats["10"] == 2):
                    players[index].modifyHandValue(score=3,value=(7+9))
                elif (stats["Jack"] == 2):
                    players[index].modifyHandValue(score=3,value=(7+10))
                elif (stats["Queen"] == 2):
                    players[index].modifyHandValue(score=3,value=(7+11))
                elif (stats["King"] == 2):
                    players[index].modifyHandValue(score=3,value=(7+12))
                elif (stats["Ace"] == 2):
                    players[index].modifyHandValue(score=3,value=(7+13))
            elif (stats["9"] == 2):
                if (stats["1"] == 2):
                    players[index].modifyHandValue(score=3,value=(8+0))
                elif (stats["2"] == 2):
                    players[index].modifyHandValue(score=3,value=(8+1))
                elif (stats["3"] == 2):
                    players[index].modifyHandValue(score=3,value=(8+2))
                elif (stats["4"] == 2):
                    players[index].modifyHandValue(score=3,value=(8+3))
                elif (stats["5"] == 2):
                    players[index].modifyHandValue(score=3,value=(8+4))
                elif (stats["6"] == 2):
                    players[index].modifyHandValue(score=3,value=(8+5))
                elif (stats["7"] == 2):
                    players[index].modifyHandValue(score=3,value=(8+6))
                elif (stats["8"] == 2):
                    players[index].modifyHandValue(score=3,value=(8+7))
                elif (stats["10"] == 2):
                    players[index].modifyHandValue(score=3,value=(8+9))
                elif (stats["Jack"] == 2):
                    players[index].modifyHandValue(score=3,value=(8+10))
                elif (stats["Queen"] == 2):
                    players[index].modifyHandValue(score=3,value=(8+11))
                elif (stats["King"] == 2):
                    players[index].modifyHandValue(score=3,value=(8+12))
                elif (stats["Ace"] == 2):
                    players[index].modifyHandValue(score=3,value=(8+13))
            elif (stats["10"] == 2):
                if (stats["1"] == 2):
                    players[index].modifyHandValue(score=3,value=(9+0))
                elif (stats["2"] == 2):
                    players[index].modifyHandValue(score=3,value=(9+1))
                elif (stats["3"] == 2):
                    players[index].modifyHandValue(score=3,value=(9+2))
                elif (stats["4"] == 2):
                    players[index].modifyHandValue(score=3,value=(9+3))
                elif (stats["5"] == 2):
                    players[index].modifyHandValue(score=3,value=(9+4))
                elif (stats["6"] == 2):
                    players[index].modifyHandValue(score=3,value=(9+5))
                elif (stats["7"] == 2):
                    players[index].modifyHandValue(score=3,value=(9+6))
                elif (stats["8"] == 2):
                    players[index].modifyHandValue(score=3,value=(9+7))
                elif (stats["9"] == 2):
                    players[index].modifyHandValue(score=3,value=(9+8))
                elif (stats["Jack"] == 2):
                    players[index].modifyHandValue(score=3,value=(9+10))
                elif (stats["Queen"] == 2):
                    players[index].modifyHandValue(score=3,value=(9+11))
                elif (stats["King"] == 2):
                    players[index].modifyHandValue(score=3,value=(9+12))
                elif (stats["Ace"] == 2):
                    players[index].modifyHandValue(score=3,value=(9+13))
            elif (stats["Jack"] == 2):
                if (stats["1"] == 2):
                    players[index].modifyHandValue(score=3,value=(10+0))
                elif (stats["2"] == 2):
                    players[index].modifyHandValue(score=3,value=(10+1))
                elif (stats["3"] == 2):
                    players[index].modifyHandValue(score=3,value=(10+2))
                elif (stats["4"] == 2):
                    players[index].modifyHandValue(score=3,value=(10+3))
                elif (stats["5"] == 2):
                    players[index].modifyHandValue(score=3,value=(10+4))
                elif (stats["6"] == 2):
                    players[index].modifyHandValue(score=3,value=(10+5))
                elif (stats["7"] == 2):
                    players[index].modifyHandValue(score=3,value=(10+6))
                elif (stats["8"] == 2):
                    players[index].modifyHandValue(score=3,value=(10+7))
                elif (stats["9"] == 2):
                    players[index].modifyHandValue(score=3,value=(10+8))
                elif (stats["10"] == 2):
                    players[index].modifyHandValue(score=3,value=(10+9))
                elif (stats["Queen"] == 2):
                    players[index].modifyHandValue(score=3,value=(10+11))
                elif (stats["King"] == 2):
                    players[index].modifyHandValue(score=3,value=(10+12))
                elif (stats["Ace"] == 2):
                    players[index].modifyHandValue(score=3,value=(10+13))
            elif (stats["Queen"] == 2):
                if (stats["1"] == 2):
                    players[index].modifyHandValue(score=3,value=(11+0))
                elif (stats["2"] == 2):
                    players[index].modifyHandValue(score=3,value=(11+1))
                elif (stats["3"] == 2):
                    players[index].modifyHandValue(score=3,value=(11+2))
                elif (stats["4"] == 2):
                    players[index].modifyHandValue(score=3,value=(11+3))
                elif (stats["5"] == 2):
                    players[index].modifyHandValue(score=3,value=(11+4))
                elif (stats["6"] == 2):
                    players[index].modifyHandValue(score=3,value=(11+5))
                elif (stats["7"] == 2):
                    players[index].modifyHandValue(score=3,value=(11+6))
                elif (stats["8"] == 2):
                    players[index].modifyHandValue(score=3,value=(11+7))
                elif (stats["9"] == 2):
                    players[index].modifyHandValue(score=3,value=(11+8))
                elif (stats["10"] == 2):
                    players[index].modifyHandValue(score=3,value=(11+9))
                elif (stats["Jack"] == 2):
                    players[index].modifyHandValue(score=3,value=(11+10))
                elif (stats["King"] == 2):
                    players[index].modifyHandValue(score=3,value=(11+12))
                elif (stats["Ace"] == 2):
                    players[index].modifyHandValue(score=3,value=(11+13))
            elif (stats["King"] == 2):
                if (stats["1"] == 2):
                    players[index].modifyHandValue(score=3,value=(12+0))
                elif (stats["2"] == 2):
                    players[index].modifyHandValue(score=3,value=(12+1))
                elif (stats["3"] == 2):
                    players[index].modifyHandValue(score=3,value=(12+2))
                elif (stats["4"] == 2):
                    players[index].modifyHandValue(score=3,value=(12+3))
                elif (stats["5"] == 2):
                    players[index].modifyHandValue(score=3,value=(12+4))
                elif (stats["6"] == 2):
                    players[index].modifyHandValue(score=3,value=(12+5))
                elif (stats["7"] == 2):
                    players[index].modifyHandValue(score=3,value=(12+6))
                elif (stats["8"] == 2):
                    players[index].modifyHandValue(score=3,value=(12+7))
                elif (stats["9"] == 2):
                    players[index].modifyHandValue(score=3,value=(12+8))
                elif (stats["10"] == 2):
                    players[index].modifyHandValue(score=3,value=(12+9))
                elif (stats["Jack"] == 2):
                    players[index].modifyHandValue(score=3,value=(12+10))
                elif (stats["Queen"] == 2):
                    players[index].modifyHandValue(score=3,value=(12+11))
                elif (stats["Ace"] == 2):
                    players[index].modifyHandValue(score=3,value=(12+13))
            elif (stats["Ace"] == 2):
                if (stats["1"] == 2):
                    players[index].modifyHandValue(score=3,value=(13+0))
                elif (stats["2"] == 2):
                    players[index].modifyHandValue(score=3,value=(13+1))
                elif (stats["3"] == 2):
                    players[index].modifyHandValue(score=3,value=(13+2))
                elif (stats["4"] == 2):
                    players[index].modifyHandValue(score=3,value=(13+3))
                elif (stats["5"] == 2):
                    players[index].modifyHandValue(score=3,value=(13+4))
                elif (stats["6"] == 2):
                    players[index].modifyHandValue(score=3,value=(13+5))
                elif (stats["7"] == 2):
                    players[index].modifyHandValue(score=3,value=(13+6))
                elif (stats["8"] == 2):
                    players[index].modifyHandValue(score=3,value=(13+7))
                elif (stats["9"] == 2):
                    players[index].modifyHandValue(score=3,value=(13+8))
                elif (stats["10"] == 2):
                    players[index].modifyHandValue(score=3,value=(13+9))
                elif (stats["Jack"] == 2):
                    players[index].modifyHandValue(score=3,value=(13+10))
                elif (stats["Queen"] == 2):
                    players[index].modifyHandValue(score=3,value=(13+11))
                elif (stats["King"] == 2):
                    players[index].modifyHandValue(score=3,value=(13+12))

            # 2  - checking for pair
            if (stats["1"] == 2) or (stats["2"] == 2) or (stats["3"] == 2) or (stats["4"] == 2) or (stats["5"] == 2) or (stats["6"] == 2) or (stats["7"] == 2) or (stats["8"] == 2) or (stats["9"] == 2) or (stats["10"] == 2) or (stats["Jack"] == 2) or (stats["Queen"] == 2) or (stats["King"] == 2) or (stats["Ace"] == 2):
                players[index].modifyHandValue(score=2)
            
            # 1  - checking for high card - is this necessary?
            players[index].modifyHandValue(score=1)

