import math
import connectfour.Connect4Heuristics as heuristics

from connectfour.player.Connect4Player import Connect4Player as c4p

class AlphaBetaPlayer(c4p):
    def makeMove(self, field):
        move, _h = self.alphabeta(field, 4, -math.inf, math.inf, True)
        return move

    def alphabeta(self, node, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or node.isTerminal():
            return -1, heuristics.aggregatePossibleWinningLinesHeuristic(node, self.color)
        
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

    def won(self, field):
        pass

    def lost(self, field):
        pass
    
    def draw(self, field):
        pass