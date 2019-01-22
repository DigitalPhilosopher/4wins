import math

from connectfour.ai.Connect4Heuristics import aggregatePossibleWinningLinesHeuristic
from connectfour.Field import Field as fd

def minimax(currentStep, maximalDepth, playerToWin, playerToMove, field):
    gameOver = field.winningPlayer()
    availableMoves = field.availableMoves()

    if availableMoves == [] and gameOver is fd.NO_PLAYER:
        return -1, 0

    bestMove = availableMoves[0]
    bestValue = -math.inf if playerToMove == playerToWin else math.inf
    
    if not gameOver == fd.NO_PLAYER:
        return bestMove, math.inf if gameOver == playerToWin else -math.inf
    
    for move in availableMoves:
        if currentStep == maximalDepth:
            heuristicValue = aggregatePossibleWinningLinesHeuristic(field.copy().makeMove(move, playerToWin), playerToWin)
        else:
            _m, heuristicValue = minimax(currentStep+1, maximalDepth, playerToWin, fd.RED_PLAYER if playerToMove == fd.YELLOW_PLAYER else fd.YELLOW_PLAYER, field.copy().makeMove(move, playerToMove))       

        if playerToMove == playerToWin and heuristicValue > bestValue:
            bestMove = move
            bestValue = heuristicValue
        elif not playerToMove == playerToWin and heuristicValue < bestValue:
            bestMove = move
            bestValue = heuristicValue
    return bestMove, bestValue
