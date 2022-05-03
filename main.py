# packages import
from threading import local
from deck import deck
from card import card
from game import game
from player import player


p1 = player("player1",100)
p2 = player("player2",100)
newGame = game([p1,p2],5)
