# imports
from threading import local
from deck import deck
from card import card
from game import game
from player import player
from bot_player import bot_player


p1 = bot_player("Mr. Gonzalas",100)
p2 = player("Litman",100)
newGame = game([p1,p2],5,play=True)
