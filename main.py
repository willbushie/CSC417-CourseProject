# packages import
from threading import local

from deck import deck
from card import card

#newGame = game()

shownCards = []
c1 = card("Clubs","One")
shownCards.append(c1)
c2 = card("Clubs","Three")
shownCards.append(c2)
c3 = card("Diamonds","Five")
shownCards.append(c3)
c4 = card("Hearts","Seven")
shownCards.append(c4)
c5 = card("Clubs","Queen")
shownCards.append(c5)
c6 = card("Clubs","King")
shownCards.append(c6)
c7 = card("Clubs","King")
shownCards.append(c7)

for i in range(len(shownCards)):
    print(f"The {shownCards[i].getInfo()}")

# testing for hand values (which will be done inside of game.checkHands())
