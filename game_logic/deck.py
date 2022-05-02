# imports
from card import card
from random import shuffle

class deck:
    """
    Creates a single deck of 52 cards, and shuffles the list of cards.
    """
    def __init__(self) -> None:
        self.deck = self.createDeck()
    
    def createDeck(self):
        """
        Creates a list of cards and shuffles it.
        """
        cards = [
            {"suit":"Hearts","rank":"Ace"},
            {"suit":"Hearts","rank":"One"},
            {"suit":"Hearts","rank":"Two"},
            {"suit":"Hearts","rank":"Three"},
            {"suit":"Hearts","rank":"Four"},
            {"suit":"Hearts","rank":"Five"},
            {"suit":"Hearts","rank":"Six"},
            {"suit":"Hearts","rank":"Seven"},
            {"suit":"Hearts","rank":"Eight"},
            {"suit":"Hearts","rank":"Nine"},
            {"suit":"Hearts","rank":"Ten"},
            {"suit":"Hearts","rank":"Jack"},
            {"suit":"Hearts","rank":"Queen"},
            {"suit":"Hearts","rank":"King"},
            {"suit":"Diamonds","rank":"Ace"},
            {"suit":"Diamonds","rank":"One"},
            {"suit":"Diamonds","rank":"Two"},
            {"suit":"Diamonds","rank":"Three"},
            {"suit":"Diamonds","rank":"Four"},
            {"suit":"Diamonds","rank":"Five"},
            {"suit":"Diamonds","rank":"Six"},
            {"suit":"Diamonds","rank":"Seven"},
            {"suit":"Diamonds","rank":"Eight"},
            {"suit":"Diamonds","rank":"Nine"},
            {"suit":"Diamonds","rank":"Ten"},
            {"suit":"Diamonds","rank":"Jack"},
            {"suit":"Diamonds","rank":"Queen"},
            {"suit":"Diamonds","rank":"King"},
            {"suit":"Spades","rank":"Ace"},
            {"suit":"Spades","rank":"One"},
            {"suit":"Spades","rank":"Two"},
            {"suit":"Spades","rank":"Three"},
            {"suit":"Spades","rank":"Four"},
            {"suit":"Spades","rank":"Five"},
            {"suit":"Spades","rank":"Six"},
            {"suit":"Spades","rank":"Seven"},
            {"suit":"Spades","rank":"Eight"},
            {"suit":"Spades","rank":"Nine"},
            {"suit":"Spades","rank":"Ten"},
            {"suit":"Spades","rank":"Jack"},
            {"suit":"Spades","rank":"Queen"},
            {"suit":"Spades","rank":"King"},
            {"suit":"Clubs","rank":"Ace"},
            {"suit":"Clubs","rank":"One"},
            {"suit":"Clubs","rank":"Two"},
            {"suit":"Clubs","rank":"Three"},
            {"suit":"Clubs","rank":"Four"},
            {"suit":"Clubs","rank":"Five"},
            {"suit":"Clubs","rank":"Six"},
            {"suit":"Clubs","rank":"Seven"},
            {"suit":"Clubs","rank":"Eight"},
            {"suit":"Clubs","rank":"Nine"},
            {"suit":"Clubs","rank":"Ten"},
            {"suit":"Clubs","rank":"Jack"},
            {"suit":"Clubs","rank":"Queen"},
            {"suit":"Clubs","rank":"King"}]
        cardsList = []
        for c in len(range(cards)):
            currCard = card(c["suit"],c["rank"])
            cardsList.append(currCard)
        return shuffle(cardsList)

    def display(self):
        """
        Displays information the deck
        """
        pass