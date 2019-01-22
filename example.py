import connectfour as cf

game = cf.Connect4(cf.HumanPlayer, cf.AlphaBetaPlayer)
game.play()