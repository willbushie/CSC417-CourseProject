# imports
from card import card
from player import player
from holdem_calc import holdem_calc

class bot_player(player):
    """
    This is the class for an automated player (no human required).\n
    This class inherits from the player class
    """
    def turn(self,call,cards):
        """
        This method contains the actions of an automated player.
        """
        returnDict = {"action":None,"amount":0}
        
        if (len(cards) == 0):
            if (call == 0):
                returnDict["action"] = "check"
            elif (call != 0):
                self.modifyChips(call)
                returnDict["action"] = "call"
        elif (len(cards) == 3):
            hand = []
            for index in range(2):
                hand.append(self.getCard(index+1).getInfoSimple())
            simp = []
            for index in range(len(cards)):
                simp.append(cards[index].getInfoSimple())
            winningProbability = holdem_calc.calculate([simp[0],simp[1],simp[2]],False,2,None,[hand[0],hand[1]],False)
            winningProbability.pop(0)
            maxProbability = max(winningProbability)
            if (maxProbability > 0.3):
                returnDict["action"] = "raise"
                if (self.getChipValue() < 15):
                    returnDict["amount"] = self.chips
                    self.modifyChips(amount=self.chips)
                else:
                    returnDict["amount"] = (self.chips * 0.3)
                    self.modifyChips(amount=self.chips * 0.3)
            elif (maxProbability <= 0.3):
                if (call != 0):
                    returnDict["action"] = "fold"
                elif (call == 0):
                    returnDict["action"] = "check"
        elif(len(cards) == 4):
            hand = []
            for index in range(2):
                hand.append(self.getCard(index+1).getInfoSimple())
            simp = []
            for index in range(len(cards)):
                simp.append(cards[index].getInfoSimple())
            winningProbability = holdem_calc.calculate([simp[0],simp[1],simp[2],simp[3]],False,2,None,[hand[0],hand[1]],False)
            winningProbability.pop(0)
            maxProbability = max(winningProbability)
            if (maxProbability > 0.5):
                returnDict["action"] = "raise"
                if (self.getChipValue() < 15):
                    returnDict["amount"] = self.chips
                    self.modifyChips(amount=self.chips)
                else:
                    returnDict["amount"] = (self.chips * 0.4)
                    self.modifyChips(amount=self.chips * 0.4)
            elif (maxProbability <= 0.5):
                if (call != 0):
                    returnDict["action"] = "fold"
                elif (call == 0):
                    returnDict["action"] = "check"
        elif(len(cards) == 5):
            hand = []
            for index in range(2):
                hand.append(self.getCard(index+1).getInfoSimple())
            simp = []
            for index in range(len(cards)):
                simp.append(cards[index].getInfoSimple())
            winningProbability = holdem_calc.calculate([simp[0],simp[1],simp[2],simp[3],simp[4]],False,2,None,[hand[0],hand[1]],False)
            winningProbability.pop(0)
            maxProbability = max(winningProbability)
            if (maxProbability > 0.7):
                returnDict["action"] = "raise"
                if (self.getChipValue() < 15):
                    returnDict["amount"] = self.chips
                    self.modifyChips(amount=self.chips)
                else:
                    returnDict["amount"] = (self.chips * 0.5)
                    self.modifyChips(amount=self.chips * 0.5)
            elif (maxProbability <= 0.5):
                if (call != 0):
                    returnDict["action"] = "fold"
                elif (call == 0):
                    returnDict["action"] = "check"

        return returnDict
