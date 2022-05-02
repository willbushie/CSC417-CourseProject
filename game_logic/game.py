# imports
from deck import deck

class game:
    """
    The Poker Game class.
    """
    def __init__(self,players) -> None:
        self.players = players
        self.pot = 0