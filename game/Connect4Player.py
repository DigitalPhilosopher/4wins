from abc import ABC, abstractmethod

class Connect4Player(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def makeMove(self, field):
        pass
    
    @abstractmethod
    def won(self):
        pass
    
    @abstractmethod
    def lost(self):
        pass
    
    @abstractmethod
    def draw(self):
        pass
