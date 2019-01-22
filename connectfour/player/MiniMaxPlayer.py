import math

from connectfour.ai.MiniMax import minimax
from connectfour.player.Connect4Player import Connect4Player as c4p

class MiniMaxPlayer(c4p):
    def makeMove(self, field):
        move, _h = minimax(0, 4, self.color, self.color, field)
        return move

    def won(self, field):
        pass

    def lost(self, field):
        pass
    
    def draw(self, field):
        pass