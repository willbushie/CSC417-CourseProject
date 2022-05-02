# imports
from card import card

class player:
    """
    This is the player object which has the ability to play the game.
    """
    def __init__(self,label,chips) -> None:
        self.label = label
        self.chips = chips
        self.hand = {"c1":None,"c2":None}
        self.fold = False
        self.handValue = 0

    def modifyChips(self,amount):
        """
        Modify the number of chips (winning/betting).\n
        ### Notice:
        Amount needs to be listed as such:\n
        For negative amounts = `amount = -100`.\n
        For positive amounts = `amount = 100`.
        """
        self.chips =+ amount

    def modifyHand(self,card=None,empty=False):
        """
        Modify hand (giving/removing cards).
        """
        if (empty == True):
            self.hand = {"c1":None,"c2":None}
        elif (empty == False) and (card["c1"] == None) and (card != None):
            self.hand["c1"] = card
        elif (empty == False) and (card["c2"] == None) and (card != None):
            self.hand["c2"] = card
        else:
            print(f"There was an issue modifying the hand.\nPassed cards value: {card}, Passed empty value: {empty}")

    def modifyFold(self,fold=True):
        """
        This method will update a players `fold` status.
        """
        self.fold = fold

    def displayHandPretty(self,print=False):
        """
        This method prints a pretty string of the hand. If `print=False`, the method returns a string of the hand.
        """
        printout = ""
        for index in range(len(self.hand)):
            if (index == 0):
                printout =+ "The " + self.hand[index].getInfo()
            else:
                printout =+ " and " + self.hand[index].getInfo()
        if (print == True):
            print(f"Hand is: {printout}.")
        elif (print == False):
            return printout

    def turn(self,call):
        """
        This method holds the players actions when it is their turn to bet.
        """
        returnDict = {"action":None,"amount":None,"fold":False}
        print(f"Price to call is: {call}.\n Your balance: {self.chips}.\n Your hand: {self.displayHandPretty()}.")
        action = input("What would you like to do?\n Raise - Call - Fold\n")
        if (action.lower() == "call"):
            self.modifyChips(amount=-call)
            returnDict["action"] = "call"
            returnDict["amount"] = call
            return returnDict
        elif(action.lower() == "raise"):
            while(True):
                amount = input("How much would you like to raise the call by?\n")
                if (amount > 0):
                    break
                elif (amount <= 0):
                    print("This is an invalid amount to raise by. Please try again.")
            self.modifyChips(amount=-(call+amount))
            returnDict["action"] = "raise"
            returnDict["amount"] = amount
            return returnDict
        elif(action.lower() == "fold"):
            self.modifyFold()
            returnDict["fold"] = "true"
            return returnDict
    