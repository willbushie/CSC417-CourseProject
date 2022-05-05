# imports
from card import card
from player import player

class bot_player(player):
    """
    This is the class for an automated player (no human required).\n
    This class inherits from the player class
    """
    def turn(self,call,cards):
        """
        This method contains the actions of an automated player.
        """
        returnDict = {"action":None,"amount":None,"fold":False}

        return returnDict