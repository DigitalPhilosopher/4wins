import math
import connectfour.Field as fd
import connectfour.ai.Connect4Heuristics as heuristics

from connectfour.player.Connect4Player import Connect4Player as c4p

class MiniMaxPlayer(c4p):
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
                heuristicValue = heuristics.aggregatePossibleWinningLinesHeuristic(field.copy().makeMove(move, playerToWin), playerToWin)
            else:
                _m, heuristicValue = self.minimax(currentStep+1, maximalDepth, playerToWin, fd.Field.RED_PLAYER if playerToMove == fd.Field.YELLOW_PLAYER else fd.Field.YELLOW_PLAYER, field.copy().makeMove(move, playerToMove))       

            if playerToMove == playerToWin and heuristicValue > bestValue:
                bestMove = move
                bestValue = heuristicValue
            elif not playerToMove == playerToWin and heuristicValue < bestValue:
                bestMove = move
                bestValue = heuristicValue
        return bestMove, bestValue

    def won(self, field):
        pass

    def lost(self, field):
        pass
    
    def draw(self, field):
        pass