from abc import ABC, abstractmethod
import Field as fd

class Connect4Player(ABC):
    def __init__(self, color):
        self.color = color
        self.opponentColor = fd.Field.RED_PLAYER if color == fd.Field.YELLOW_PLAYER else fd.Field.YELLOW_PLAYER

    @abstractmethod
    def makeMove(self, field):
        pass
    
    @abstractmethod
    def won(self, field):
        pass
    
    @abstractmethod
    def lost(self, field):
        pass
    
    @abstractmethod
    def draw(self, field):
        pass
