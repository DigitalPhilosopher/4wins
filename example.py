import connectfour as cf

human_player = cf.player.HumanPlayer.HumanPlayer()
ai_player = cf.player.AlphaBetaPlayer.AlphaBetaPlayer()

game = cf.Connect4(human_player, ai_player)
game.play()