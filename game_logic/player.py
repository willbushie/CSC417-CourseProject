# imports
from card import card

class player:
    """
    This is the player object which has the ability to play the game.
    """
    def __init__(self,chips) -> None:
        self.chips = chips
        self.hand = []

    def modifyChips(self,amount):
        """
        Modify the number of chips (winning/betting).\n
        ### Notice:
        Amount needs to be listed as such:\n
        For negative amounts = `amount = -100`.\n
        For positive amounts = `amount = 100`.
        """
        self.chips =+ amount

    def modifyHand(self,cards=None,empty=True):
        """
        Modify hand (giving/removing cards).
        """
        if (empty == True):
            self.hand = []
        elif (empty == False) and (cards != None):
            self.hand = cards
        else:
            print(f"There was an issue modifying the hand.\nPassed cards value: {cards}, Passed empty value: {empty}")
