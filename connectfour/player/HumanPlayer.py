import connectfour.Field as fd

from tkinter import *
from connectfour.player.Connect4Player import Connect4Player as c4p


class HumanPlayer(c4p):
    def __init__(self, color):
        super(HumanPlayer, self).__init__(color)

        self.master = Tk()

        self.window = Canvas(self.master, width=self.FIELD_WINDOW_LENGTH*fd.Field.FIELD_LENGTH, height=100*fd.Field.FIELD_HEIGHT)
        self.window.pack()

        self.master.bind('<Motion>', self.movePossiblePiece)
        self.master.bind('<Button-1>', self.choosePosition)

        self.field = fd.Field()

        self.master.update_idletasks()
        self.master.update()

    FIELD_WINDOW_LENGTH = 100
    FIELD_WINDOW_HEIGHT = 100
    
    pointerLength = 0
    pointerHeight = 0

    def movePossiblePiece(self, event):
        pointerPosition = int(event.x/self.FIELD_WINDOW_LENGTH)
        pointerHeight = self.field.getHeightForMove(pointerPosition)
        self.window.move("pointer", (pointerPosition - self.pointerLength) * self.FIELD_WINDOW_LENGTH, (pointerHeight - self.pointerHeight) * self.FIELD_WINDOW_HEIGHT)
        self.pointerLength = pointerPosition
        self.pointerHeight = pointerHeight
    
    def choosePosition(self, event):
        self.move = int(event.x/self.FIELD_WINDOW_LENGTH)
        self.sem.release()
    
    def drawField(self):
        for height in range(fd.Field.FIELD_HEIGHT):
            for length in range(fd.Field.FIELD_LENGTH):
                self.window.create_rectangle(length*self.FIELD_WINDOW_LENGTH, height*self.FIELD_WINDOW_HEIGHT, self.FIELD_WINDOW_LENGTH+length*self.FIELD_WINDOW_LENGTH, self.FIELD_WINDOW_HEIGHT+height*self.FIELD_WINDOW_HEIGHT, fill="blue")
                if self.field.getField()[height][length] == fd.Field.RED_PLAYER:
                    self.window.create_oval(length*self.FIELD_WINDOW_LENGTH, height*self.FIELD_WINDOW_HEIGHT, self.FIELD_WINDOW_LENGTH+length*self.FIELD_WINDOW_LENGTH, self.FIELD_WINDOW_HEIGHT+height*self.FIELD_WINDOW_HEIGHT, fill="red")
                elif self.field.getField()[height][length] == fd.Field.YELLOW_PLAYER:
                    self.window.create_oval(length*self.FIELD_WINDOW_LENGTH, height*self.FIELD_WINDOW_HEIGHT, self.FIELD_WINDOW_LENGTH+length*self.FIELD_WINDOW_LENGTH, self.FIELD_WINDOW_HEIGHT+height*self.FIELD_WINDOW_HEIGHT, fill="yellow")

    def makeMove(self, field):
        self.sem = threading.Semaphore()
        self.sem.acquire()
        self.field = field
        self.drawField()
        self.master.update()
        self.window.create_oval(0*self.FIELD_WINDOW_LENGTH, 0*self.FIELD_WINDOW_HEIGHT, self.FIELD_WINDOW_LENGTH+0*self.FIELD_WINDOW_LENGTH, self.FIELD_WINDOW_HEIGHT+0*self.FIELD_WINDOW_HEIGHT, fill="yellow", tag="pointer")


        self.sem.acquire()
        return self.move
    
    def won(self):
        print("You won")

    def lost(self):
        print("You lost")
    
    def draw(self):
        print("Nobody won")
