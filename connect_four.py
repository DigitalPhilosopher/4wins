import arcade
import connectfour.Field as fd

MARGIN = 15
RADIUS = 25

SCREEN_WIDTH = (2 * RADIUS + MARGIN) * fd.Field.FIELD_LENGTH + MARGIN
SCREEN_HEIGHT = (2 * RADIUS + MARGIN) * (fd.Field.FIELD_HEIGHT + 1) + MARGIN
PICK_ROW = (2 * RADIUS + MARGIN) * fd.Field.FIELD_HEIGHT + MARGIN + RADIUS



class ConnectFour(arcade.Window):
    
    def __init__(self, width, height):

        super().__init__(width, height)

        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.BLUE)

        self.field = fd.Field()

        self.position_x = 50
    

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
                elif field[row][column] == fd.Field.YELLOW_PLAYER:
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
        move = self.get_pick_from_position()
        self.field.makeMove(move, fd.Field.RED_PLAYER)
        



def main():
    ConnectFour(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()



if __name__ == "__main__":
    main()
