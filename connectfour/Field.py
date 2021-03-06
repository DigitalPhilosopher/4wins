import numpy as np

class Field:
    NO_PLAYER = 0
    RED_PLAYER = 1
    YELLOW_PLAYER = 2

    FIELD_LENGTH = 7
    FIELD_HEIGHT = 6


    def __init__(self, field = None):
        if field is None:
            self.field = self.initializeField()
        else:
            self.field = field


    def initializeField(self):
        return np.full([self.FIELD_HEIGHT, self.FIELD_LENGTH], self.NO_PLAYER)


    def winningPlayer(self):
        for elementsInDiagonal in [set(possibleLine) for possibleLine in self.possible_winning_lines()]:
            firstElement = elementsInDiagonal.pop()
            if len(elementsInDiagonal) == 0 and firstElement != self.NO_PLAYER:
                return firstElement
        return self.NO_PLAYER


    def horizontal_lines(self):
        return [list(row) for row in self.field]


    def vertical_lines(self):
        return [list(col) for col in self.field.T]


    def diagonal_lines(self):
        lines = []
        lines.extend([list(self.field.diagonal(i)) for i in range(-2,4)])
        lines.extend([list(self.field[::-1,:].diagonal(i)) for i in range(-2,4)])

        return lines
    

    def crop_lines(self, lines):
        for line in lines:
            while len(line) > 4:
                lines.append(line[0:4])
                line.remove(line[0])
        
        return lines


    def possible_winning_lines(self):
        lines = []
        lines.extend(self.horizontal_lines())
        lines.extend(self.vertical_lines())
        lines.extend(self.diagonal_lines())

        return self.crop_lines(lines)


    def moveIsValid(self, move):
        if move >= len(self.field[0]) or move < 0:
            return False
        if not self.field[0][move] == self.NO_PLAYER:
            return False
        return True


    def availableMoves(self):
        possibleMoves = []
        for move in range(self.FIELD_LENGTH):
            if (self.moveIsValid(move)):
                possibleMoves.append(move)
        return possibleMoves


    def boardIsFull(self):
        for col in range(len(self.field[0])):
            if self.field[0][col] == self.NO_PLAYER:
                return False
        return True


    def makeMove(self, move, player):
        for row in reversed(range(len(self.field))):
            if self.field[row][move] == self.NO_PLAYER:
                self.field[row][move] = player
                return self


    def getHeightForMove(self, move):
        for row in reversed(range(len(self.field))):
            if self.field[row][move] == self.NO_PLAYER:
                return row
        return -1


    def isTerminal(self):
        return self.boardIsFull() or self.winningPlayer()


    def copy(self):
        return Field(self.field.copy())


    def getField(self):
        return self.field.copy()
