import math
from collections import Counter

import connectfour.Connect4Player as c4p
import connectfour.Field as fd

class MiniMaxPlayer(c4p.Connect4Player):
    def makeMove(self, field):
        move, _h = self.minimax(0, 4, self.color, self.color, field)
        return move

    def minimax(self, currentStep, maximalDepth, playerToWin, playerToMove, field):
        gameOver = field.winningPlayer()
        availableMoves = field.availableMoves()

        if availableMoves == [] and gameOver is fd.Field.NO_PLAYER:
            return -1, 0

        bestMove = availableMoves[0]
        bestValue = -math.inf if playerToMove == playerToWin else math.inf
        
        if not gameOver == fd.Field.NO_PLAYER:
            return bestMove, math.inf if gameOver == playerToWin else -math.inf
        
        for move in availableMoves:
            if currentStep == maximalDepth:
                heuristicValue = self.heuristic(field.copy().makeMove(move, playerToWin), playerToWin)
            else:
                _m, heuristicValue = self.minimax(currentStep+1, maximalDepth, playerToWin, fd.Field.RED_PLAYER if playerToMove == fd.Field.YELLOW_PLAYER else fd.Field.YELLOW_PLAYER, field.copy().makeMove(move, playerToMove))       

            if playerToMove == playerToWin and heuristicValue > bestValue:
                bestMove = move
                bestValue = heuristicValue
            elif not playerToMove == playerToWin and heuristicValue < bestValue:
                bestMove = move
                bestValue = heuristicValue
        return bestMove, bestValue

    def heuristic(self, field, player):
        opponent = fd.Field.RED_PLAYER if player == fd.Field.YELLOW_PLAYER else fd.Field.YELLOW_PLAYER
        arrayField = field.getField()

        possibleLines = [list(row) for row in arrayField]
        possibleLines.extend([list(col) for col in arrayField.T])
        possibleLines.extend([list(arrayField.diagonal(i)) for i in range(-2,4)])
        possibleLines.extend([list(arrayField[::-1,:].diagonal(i)) for i in range(-2,4)])
        for possibleLine in possibleLines:
            while len(possibleLine) > 4:
                possibleLines.append(possibleLine[0:4])
                possibleLine.remove(possibleLine[0])
        
        value = 0
        for line in possibleLines:
            count = Counter(line)
            if player in count:
                if not opponent in count:
                    value += count[player] ** 2
            elif opponent in count:
                value -= count[opponent] ** 3
        return value

    def won(self, field):
        pass

    def lost(self, field):
        pass
    
    def draw(self, field):
        pass