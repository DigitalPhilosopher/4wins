import Field as fd

class Connect4:
    def __init__(self, playerRedFunction, playerYellowFunction):
        self.field = fd.Field()
        
        # TODO: Check if it is the right class
        self.playerRedFunction = playerRedFunction(fd.Field.RED_PLAYER)
        self.playerYellowFunction = playerYellowFunction(fd.Field.YELLOW_PLAYER)
        
        self.playerForTurn = fd.Field.RED_PLAYER
        self.playerFunction = self.playerRedFunction
    
    def play(self):
        while not self.field.winningPlayer() and self.field.boardIsFull():
            print(self.field.getField())
            move = self.playerFunction.makeMove(self.field.copy())
            while not self.field.moveIsValid(move):
                move = self.playerFunction.makeMove(self.field.copy())
            self.field.makeMove(move, self.playerForTurn)

            if self.playerForTurn == fd.Field.RED_PLAYER:
                self.playerForTurn = fd.Field.YELLOW_PLAYER
                self.playerFunction = self.playerYellowFunction
            else:
                self.playerForTurn = fd.Field.RED_PLAYER
                self.playerFunction = self.playerRedFunction
        
        if self.field.winningPlayer() == fd.Field.NO_PLAYER:
            print("Game over! No winning player.")
        else:
            print("Game over! Winner is player " + ("red" if self.field.winningPlayer() == fd.Field.RED_PLAYER else "yellow") + ".")
            if self.field.winningPlayer() == fd.Field.RED_PLAYER:
                self.playerRedFunction.won()
                self.playerYellowFunction.lost()
            else:
                self.playerRedFunction.lost()
                self.playerYellowFunction.won()
