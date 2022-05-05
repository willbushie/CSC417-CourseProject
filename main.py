# imports
from threading import local
from deck import deck
from card import card
from game import game
from player import player
from bot_player import bot_player


""" p1 = player("Luke",100)
p2 = player("Bushie",100)
p3 = player("player3",100)
newGame = game([p1,p2],5,play=True) """

# create player
p1 = player("Luke",100)
# create cards
c1 = card("Spades","One")
c2 = card("Spades","Two")
c4 = card("Spades","Three")
c5 = card("Spades","Ace")
c6 = card("Spades","Five")
c7 = card("Spades","Six")
c3 = card("Spades","Seven")
# modify the hand 
p1.modifyHand(c1)
p1.modifyHand(c2)
cardsList = [c3, c4, c5, c6, c7]
newGame = game([p1],5,play=False,cards=cardsList)
p1.display()

# use decision trees for this project
# if the probability of winning is low, fold
# if the probability of winning decreased, fold

