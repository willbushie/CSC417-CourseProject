# imports
from card import card
from player import player

class bot_player(player):
    """
    This is the class for an automated player (no human required).\n
    This class inherits from the player class
    """
    def turn(self,call):
        """
        This method contains the actions of an automated player.
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
            self.modifyFold()
            returnDict["fold"] = "true"
            print(f"Player {self.label} has chosen to fold. Remaining chips: {self.chips}.")
            return returnDict
