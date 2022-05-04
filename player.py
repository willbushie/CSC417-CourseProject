# imports
from card import card

class player:
    """
    This is the player object which has the ability to play the game via command line (requires human).
    """
    def __init__(self,label,chips) -> None:
        self.label = label
        self.chips = chips
        self.hand = {"c1":None,"c2":None}
        self.callStatus = False
        self.handValue = 0

    def modifyChips(self,amount,transactionType=0):
        """
        Modify the number of chips (winning/betting).\n
        ### Notice:
        Amount needs to be listed as such:\n
        For negative amounts = `transactionType = 0`.\n
        For positive amounts = `transactionType = 1`.\n
        Default `transactionType=0`.
        """
        if (transactionType == 0):
            self.chips = self.chips - amount
        elif (transactionType == 1):
            self.chips = self.chips + amount

    def modifyHand(self,card=None,empty=False):
        """
        Modify hand (giving/removing cards).
        """
        if (empty == True):
            self.hand = {"c1":None,"c2":None}
        elif (empty == False) and (self.hand["c1"] == None) and (card != None):
            self.hand["c1"] = card
        elif (empty == False) and (self.hand["c2"] == None) and (card != None):
            self.hand["c2"] = card
        else:
            print(f"There was an issue modifying the hand.\nPassed cards value: {card}, Passed empty value: {empty}")

    def modifyCallSatus(self,status=False):
        """
        This method will update a players `callSatus`. Default is `callStatus=False`.
        """
        self.callSatus = status

    def modifyHandValue(self,value=0):
        """
        Modify self.handVaue to evaluate winning positions.\n Default parameter is: `value=0`
        """
        if (value == 0):
            self.handValue = 0
        elif (value != 0):
            self.handValue = max(value,self.handValue)

    def displayHandPretty(self,print=False):
        """
        This method prints a pretty string of the hand. If `print=False`, the method returns a string of the hand.
        """
        printout = f"The {self.hand['c1'].getInfo()} and the {self.hand['c2'].getInfo()}"
        if (print == True):
            print(f"Hand is: {printout}.")
        elif (print == False):
            return printout

    def turn(self,call):
        """
        This method holds the players actions when it is their turn to bet.
        """
        returnDict = {"action":None,"amount":None,"fold":False}
        print(f"Player {self.label}:")
        print(f"Price to call is: {call}.\n Your balance: {self.chips}.\n Your hand: {self.displayHandPretty()}.")
        action = input("What would you like to do?\n Raise - Call - Fold\n")
        if (action.lower() == "call"):
            self.modifyChips(amount=call)
            returnDict["action"] = "call"
            returnDict["amount"] = call
            print(f"Player {self.label} has chosen to call. Remaining chips: {self.chips}.")
            return returnDict
        elif(action.lower() == "raise"):
            while(True):
                amount = int(input("How much would you like to raise the call by?\n"))
                if (amount > 0):
                    break
                elif (amount <= 0):
                    print("This is an invalid amount to raise by. Please try again.")
            totalBet = call + amount
            self.modifyChips(amount=totalBet,transactionType=0)
            returnDict["action"] = "raise"
            returnDict["amount"] = amount
            print(f"Player {self.label} has chosen to raise. Remaining chips: {self.chips}.")
            return returnDict
        elif(action.lower() == "fold"):
            returnDict["fold"] = "true"
            print(f"Player {self.label} has chosen to fold. Remaining chips: {self.chips}.")
            return returnDict
    
    def getHandValue(self):
        """
        Return the `handValue` for the player object.
        """
        return self.handValue

    def getLabel(self):
        """
        Return a string of the player label.
        """
        return self.label

    def getCard(self,card=1):
        """
        Get one of the cards from the player hand. Enter `1` for "c1" and `2` for "c2".\n
        Card object is returned
        """
        if (card == 1):
            return self.hand["c1"]
        elif (card == 2):
            return self.hand["c2"]

    def resetState(self):
        """
        This method will reset all of the correct items between rounds.
        """
        self.modifyCallSatus()
        self.modifyHand(empty=True)
        self.modifyHandValue()