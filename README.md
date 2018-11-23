# Connect4

This is a project to develop an artificial intelligence (AI) for the famous perfect information game connect4. The code is written in python3 and utilizes tkinter for the graphical user interface. The AI algorithms used to solve the game are the MiniMax algorithm and the AlphaBetaPruning algorithm. Both algorithms use the same heuristic to define the state of the board.


## The game

"Connect Four" is a board game originaly puplished by  Milton Bradley in 1974 [1]. This is a two player game, similar to tic-tac-toe in which the players have full information about the game at every point. For that reason the game is a "perfect information" game.
<br />
Connect four has a field which has a length of 7 and a height of 6. The players choose in turns where to place their next piece, until one player has achieved to have four pieces in a row.
<br />

| Connect Four | Alpha Beta AI wins against human |
| :-: | :-: |
| ![Picture of Connect Four - Alpha Beta AI wins against human](photos/ConnectFourAlphaBetaPruningWins1.png?raw=true "Connect Four - Alpha Beta AI wins against human") | ![Picture of Connect Four - Alpha Beta AI wins against human](photos/ConnectFourAlphaBetaPruningWins2.png?raw=true "Connect Four - Alpha Beta AI wins against human") |


## Artificial Intelligence (AI)
In today's world, the utilization of artificial intelligence (AI) to solve problems becomes more and more important. Humans discover new and more difficult problems every day. These can not be solved by humans themeselves any more. For that reason AI is needed to support humans in problem solving and pushing society towards the future.

### Heuristic for "Connect Four"
The heuristic for "Connect Four" is needed for the following AI algorithms, to calculate the value of the field. This value defines, how high the possibility is for the player to win. The algorithm returns -inf, if the game is lost and +inf if the player wins. to evaluate the a status, where no player has won yet, the algorithm iterates over every possible field, with which a player could win the game. If no player or both have a piece in this field, the value is zero. If the field only consists of the pieces from one player, the number of pieces decides, how much is added or subtracted from the final value. If the opponent has pieces in the field, the number of pieces by the power of 3 is subtracted from the final value. Otherwise, the number of pieces by the power of 2 is added to the final value.
<br />
The fields filled with the pieces of the opponent are valued more, for the reason that the algorithm does not want to run in a situation, where it can not win anymore. Therefore it is more important to minimize the opponent first and afterwards maximize the value.

### Minimax
The minimax algorithm is a algorithm which can be used for two player games in decision making. The algorithm looks into the possible moves and evaluates the best value. For each move the algorithm maximizes or minimizes the value of the field, based on which player has the turn. Considering the following decision tree, where a red node displays the turn of the maximizer and the green node displays the turn of the minimizer. The values at the leafs are the values of the field at the end:
<br />
![Decision Tree minimax algorithm](photos/DecisionTreeMinimax.png?raw=true "Decision tree minimax algorithm")
<br />
The minimizer in the second generation would try to minimize the value of the field, so that the opponent has a worse position. Therefore the left turn in the left node, resulting in the value of 5 and the right turn in the right node, resulting in the value 3 are the best possible decision for the minimizer. The maximizer displayed in the root can then choose between the values 5 on the left path and 3 on the right path. Since a maximal value is wanted, the maximizer chooses the left path, resulting in the value 5.
<br />
![Decision Tree minimax algorithm](photos/DecisionTreeMinimaxPath.png?raw=true "Decision tree minimax algorithm")

### Alpha-beta pruning
The alpha-beta pruning algorithm is based on the minimax algorithm. The algorithm uses two values, alpha and beta to store the best value which can be guaranteed by the maximizer and the minimizer. That enables the algorithm skipping parts of the tree which would definetely result in higher (or lower) values.


## References

1. “4 In A Line!” Correlation, www.mathsisfun.com/games/connect4.html.