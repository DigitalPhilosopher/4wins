from tkinter import *
from collections import Counter
import math
import numpy as np


_FREE = 0
_RED = 1
_YELLOW = 2

_FIELDLENGTH = 7
_FIELDHEIGHT = 6

def initializeField():
    return np.full([_FIELDHEIGHT, _FIELDLENGTH], _FREE)

def checkPlayerWon(field):
    possibleLines = [list(row) for row in field]
    possibleLines.extend([list(col) for col in field.T])
    possibleLines.extend([list(field.diagonal(i)) for i in range(-2,4)])
    possibleLines.extend([list(field[::-1,:].diagonal(i)) for i in range(-2,4)])
    for possibleLine in possibleLines:
        while len(possibleLine) > 4:
            possibleLines.append(possibleLine[0:4])
            possibleLine.remove(possibleLine[0])
    
    for elementsInDiagonal in [set(possibleLine) for possibleLine in possibleLines]:
        firstElement = elementsInDiagonal.pop()
        if len(elementsInDiagonal) == 0 and firstElement != _FREE:
            return firstElement
    return _FREE

def checkMoveIsValid(field, move):
    if move >= len(field[0]) or move < 0:
        return False
    if not field[0][move] == _FREE:
        return False
    return True

def checkValidMovesAvailable(field):
    for col in range(len(field[0])):
        if field[0][col] == _FREE:
            return True
    return False

# TODO: field as own class
def makeMove(field, move, player):
    for row in reversed(range(len(field))):
        if field[row][move] == _FREE:
            field[row][move] = player
            return field

def play(playerRedFunction, playerYellowFunction):
    field = initializeField()
    player = _RED
    playerFunction = playerRedFunction
    while not checkPlayerWon(field) and checkValidMovesAvailable(field):
        move = playerFunction(field.copy(), player)
        while not checkMoveIsValid(field, move):
            move = playerFunction(field.copy(), player)
        makeMove(field, move, player)

        if player == _RED:
            player = _YELLOW
            playerFunction = playerYellowFunction
        else:
            player = _RED
            playerFunction = playerRedFunction
    
    print("Game over Winner is")
    print(checkPlayerWon(field))

def getMoves(field):
    possibleMoves = []
    for move in range(_FIELDLENGTH):
        if (checkMoveIsValid(field, move)):
            possibleMoves.append(move)
    return possibleMoves

def minimax(currentStep, maximalDepth, playerToWin, playerToMove, field):
    bestMove = getMoves(field)[0]
    bestValue = -math.inf if playerToMove == playerToWin else math.inf
    
    gameOver = checkPlayerWon(field)
    if not gameOver == _FREE:
        return bestMove, math.inf if gameOver == playerToWin else -math.inf
    
    for move in getMoves(field):
        if currentStep == maximalDepth:
            heuristicValue = heuristic(makeMove(field.copy(), move, playerToWin), playerToWin)
        else:
            _m, heuristicValue = minimax(currentStep+1, maximalDepth, playerToWin, _RED if playerToMove == _YELLOW else _YELLOW, makeMove(field.copy(), move, playerToMove))       

        if playerToMove == playerToWin and heuristicValue > bestValue:
            bestMove = move
            bestValue = heuristicValue
        elif not playerToMove == playerToWin and heuristicValue < bestValue:
            bestMove = move
            bestValue = heuristicValue
    return bestMove, bestValue

def heuristic(field, player):
    opponent = _RED if player == _YELLOW else _YELLOW

    possibleLines = [list(row) for row in field]
    possibleLines.extend([list(col) for col in field.T])
    possibleLines.extend([list(field.diagonal(i)) for i in range(-2,4)])
    possibleLines.extend([list(field[::-1,:].diagonal(i)) for i in range(-2,4)])
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
            value -= count[opponent] ** 2
    return value

def playerMove(field, color):
    print(field)
    return int(input("Pick a move! > "))

def normalAI(field, color):
    move, _h = minimax(0, 4, color, color, field)
    return move

play(playerMove, normalAI)
