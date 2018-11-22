import math
import Connect4Player as c4p
import Field as fd
from collections import Counter

class AlphaBetaPlayer(c4p.Connect4Player):
    def makeMove(self, field):
        move, _h = self.alphabeta(field, 4, -math.inf, math.inf, True)
        return move

    def alphabeta(self, node, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or node.isTerminal():
            return -1, self.heuristic(node, self.color)
        
        availableMoves = node.availableMoves()
        bestMove = availableMoves[0]

        if maximizingPlayer:
            value = -math.inf
            for move in availableMoves:
                _m, heuristic = self.alphabeta(node.copy().makeMove(move, self.color), depth - 1, alpha, beta, False)
                if value < heuristic:
                    value = heuristic
                    bestMove = move
                alpha = max(value, alpha)
                if alpha >= beta:
                    break
            return bestMove, value
        
        else:
            value = math.inf
            for move in availableMoves:
                _m, heuristic = self.alphabeta(node.copy().makeMove(move, self.opponentColor), depth - 1, alpha, beta, True)
                if value > heuristic:
                    value = heuristic
                    bestMove = move
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return bestMove, value

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
                    if count[player] == 4:
                        return math.inf
            elif opponent in count:
                if count[opponent] == 4:
                    return -math.inf
                value -= count[opponent] ** 3
        return value

    def won(self, field):
        pass

    def lost(self, field):
        pass
    
    def draw(self, field):
        pass