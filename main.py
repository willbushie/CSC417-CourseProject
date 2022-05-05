# imports
from threading import local
from deck import deck
from card import card
from game import game
from player import player
from bot_player import bot_player


p1 = player("Luke",100)
p2 = player("Bushie",100)
p3 = player("player3",100)
newGame = game([p1,p2],5,play=True)


# use decision trees for this project
# if the probability of winning is low, fold
# if the probability of winning decreased, fold

