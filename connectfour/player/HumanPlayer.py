import tkinter as tk
import connectfour.Field as fd

from connectfour.player.Connect4Player import Connect4Player as c4p

class HumanPlayer(c4p):
    FIELD_WINDOW_LENGTH = 100
    FIELD_WINDOW_HEIGHT = 100

    def __init__(self, color):
        super(HumanPlayer, self).__init__(color)

        self.master = tk.Tk()
        self.master.title("Connect Four")

        self.window = tk.Canvas(
            self.master,
            width = self.FIELD_WINDOW_LENGTH*fd.Field.FIELD_LENGTH,
            height = self.FIELD_WINDOW_HEIGHT*fd.Field.FIELD_HEIGHT
        )

        self.window.pack()
        
    def choosePosition(self, event):
        move = int(event.x / self.FIELD_WINDOW_LENGTH)
        if move < fd.Field.FIELD_LENGTH and move >= 0:
            self.move = move
            self.moveDecided = True
        self.drawWindow()

    def drawWindow(self):
        self.drawField()
        self.master.update_idletasks()
        self.master.update()

    def drawField(self):
        for height in range(fd.Field.FIELD_HEIGHT):
            for length in range(fd.Field.FIELD_LENGTH):
                self.window.create_rectangle(
                    length*self.FIELD_WINDOW_LENGTH,
                    height*self.FIELD_WINDOW_HEIGHT,
                    self.FIELD_WINDOW_LENGTH+length*self.FIELD_WINDOW_LENGTH,
                    self.FIELD_WINDOW_HEIGHT+height*self.FIELD_WINDOW_HEIGHT,
                    fill="blue"
                )
                if self.field.getField()[height][length] == fd.Field.RED_PLAYER:
                    self.window.create_oval(
                        length*self.FIELD_WINDOW_LENGTH,
                        height*self.FIELD_WINDOW_HEIGHT,
                        self.FIELD_WINDOW_LENGTH+length*self.FIELD_WINDOW_LENGTH,
                        self.FIELD_WINDOW_HEIGHT+height*self.FIELD_WINDOW_HEIGHT,
                        fill="red"
                    )
                elif self.field.getField()[height][length] == fd.Field.YELLOW_PLAYER:
                    self.window.create_oval(
                        length*self.FIELD_WINDOW_LENGTH,
                        height*self.FIELD_WINDOW_HEIGHT,
                        self.FIELD_WINDOW_LENGTH+length*self.FIELD_WINDOW_LENGTH,
                        self.FIELD_WINDOW_HEIGHT+height*self.FIELD_WINDOW_HEIGHT,
                        fill="yellow"
                    )

    def makeMove(self, field):
        self.field = field
        self.possibleMove = None
        self.moveDecided = False
        self.window.bind("<Button-1>", self.choosePosition)
        while not self.moveDecided:
            self.drawWindow()
        self.window.unbind("<Button 1>")
        return self.move
    
    def won(self, field):
        self.field = field
        self.drawFinal()

    def lost(self, field):
        self.field = field
        self.drawFinal()
    
    def draw(self, field):
        self.field = field
        self.drawFinal()
    
    def drawFinal(self):
        self.window.unbind("<Motion>")
        self.window.unbind("<Button-1>")
        self.drawWindow()
        tk.mainloop()
