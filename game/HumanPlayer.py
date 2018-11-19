import Connect4Player as c4p

class HumanPlayer(c4p.Connect4Player):
    def makeMove(self, field):
        print(field.getField())
        return int(input("Pick a move! > "))
    
    def won(self):
        print("You won")

    def lost(self):
        print("You lost")
    
    def draw(self):
        print("Nobody won")
