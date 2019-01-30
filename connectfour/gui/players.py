
from connectfour.player.Connect4Player import Connect4Player as c4p
from connectfour.player.AlphaBetaPlayer import AlphaBetaPlayer as abp
from connectfour.player.MiniMaxPlayer import MiniMaxPlayer as mmp

class HumanPlayer(c4p):
    def __init__(self, function_holder):
        super(HumanPlayer, self).__init__()

        self.function_holder = function_holder

    def makeMove(self, field):
        return self.function_holder.make_move(field, self.color)
    
    def won(self, field):
        self.function_holder.won(field, self.color)

    def lost(self, field):
        self.function_holder.lost(field, self.color)
    
    def draw(self, field):
        self.function_holder.draw(field, self.color)

class AlphaBetaPlayer(abp):
    def __init__(self, function_holder):
        super(AlphaBetaPlayer, self).__init__()

        self.function_holder = function_holder

    def makeMove(self, field):
        move = super().makeMove(field)

        self.function_holder.field.makeMove(move, self.color)

        return move
    
    def won(self, field):
        super().won(field)
        self.function_holder.won(field, self.color)

    def lost(self, field):
        super().lost(field)
        self.function_holder.lost(field, self.color)
    
    def draw(self, field):
        super().draw(field)
        self.function_holder.draw(field, self.color)

class MiniMaxPlayer(mmp):
    def __init__(self, function_holder):
        super(MiniMaxPlayer, self).__init__()

        self.function_holder = function_holder

    def makeMove(self, field):
        move = super().makeMove(field)

        self.function_holder.field.makeMove(move, self.color)

        return move
    
    def won(self, field):
        super().won(field)
        self.function_holder.won(field, self.color)

    def lost(self, field):
        super().lost(field)
        self.function_holder.lost(field, self.color)
    
    def draw(self, field):
        super().draw(field)
        self.function_holder.draw(field, self.color)
