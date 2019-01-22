import math
import connectfour.Field as fd

from collections import Counter

def aggregatePossibleWinningLinesHeuristic(field, player):
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
                if count[player] == 4:
                    return math.inf
        elif opponent in count:
            if count[opponent] == 4:
                return -math.inf
            value -= count[opponent] ** 3
    return value