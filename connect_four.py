import arcade, queue, threading
import connectfour.Field as fd
import connectfour.Connect4 as cf
from connectfour.player.Connect4Player import Connect4Player as c4p

MARGIN = 15
RADIUS = 25

SCREEN_WIDTH = (2 * RADIUS + MARGIN) * fd.Field.FIELD_LENGTH + MARGIN
SCREEN_HEIGHT = (2 * RADIUS + MARGIN) * (fd.Field.FIELD_HEIGHT + 1) + MARGIN
PICK_ROW = (2 * RADIUS + MARGIN) * fd.Field.FIELD_HEIGHT + MARGIN + RADIUS

sem = threading.Semaphore()


class HumanPlayer(c4p):
    def __init__(self, func):
        super(HumanPlayer, self).__init__()

        self.func = func

    def makeMove(self, field):
        return self.func.make_move(field)
    
    def won(self, field):
        pass

    def lost(self, field):
        pass
    
    def draw(self, field):
        pass
    
    def drawFinal(self):
        pass




class ConnectFour(arcade.Window):
    
    def __init__(self, width, height):

        super().__init__(width, height)

        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.BLUE)

        self.field = fd.Field()

        self.player = HumanPlayer(self)
        self.oplayer = HumanPlayer(self)

        self.position_x = 50

        sem.acquire()
        game = cf(self.player, self.oplayer)
        t = threading.Thread(target=game.play)
        t.daemon = True
        t.start()

    

    def make_move(self, field):
        self.field = field
        print(field.getField())

        sem.acquire()
        ret = self.move
        
        return ret

    def on_draw(self):
        arcade.start_render()

        self.draw_grid()

        arcade.draw_circle_filled(self.position_x, PICK_ROW, RADIUS, arcade.color.YELLOW)
    

    def draw_grid(self):
        field = self.field.getField()
        for row in range(fd.Field.FIELD_HEIGHT):
            for column in range(fd.Field.FIELD_LENGTH):
                if field[fd.Field.FIELD_HEIGHT - row - 1][column] == fd.Field.RED_PLAYER:
                    color = arcade.color.RED
                elif field[fd.Field.FIELD_HEIGHT - row - 1][column] == fd.Field.YELLOW_PLAYER:
                    color = arcade.color.YELLOW
                else:
                    color = arcade.color.BABY_BLUE

                x = (MARGIN + 2 * RADIUS) * column + MARGIN + RADIUS
                y = (MARGIN + 2 * RADIUS) * row + MARGIN + RADIUS

                arcade.draw_circle_filled(x, y, RADIUS, color)
    

    def on_mouse_motion(self, x, y, dx, dy):
        self.position_x = x
        for column in range(fd.Field.FIELD_LENGTH):
            center = (column + 1) * MARGIN + column * 2 * RADIUS + RADIUS
            left = center - RADIUS
            right = center + RADIUS
            if x > left and x < right:
                self.position_x = center
    

    def get_pick_from_position(self):
        column = 0

        x = self.position_x
        while x > (MARGIN + RADIUS):
            column += 1
            x -= (2 * RADIUS + MARGIN)
        
        return column
    

    def on_mouse_release(self, x, y, dx, dy):
        self.move = self.get_pick_from_position()
        sem.release()
        



def main():
    ConnectFour(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()



if __name__ == "__main__":
    main()
