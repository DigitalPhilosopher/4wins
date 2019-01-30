
from connectfour.player.Connect4Player import Connect4Player as c4p

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