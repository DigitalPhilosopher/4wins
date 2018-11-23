import connectfour as cf

game = cf.Connect4(cf.HumanGUIPlayer, cf.AlphaBetaPlayer)
game.play()