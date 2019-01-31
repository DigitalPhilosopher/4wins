import arcade
from threading import Semaphore, Thread
from connectfour.gui.scene import Scene
import connectfour.Field as fd
import connectfour.Connect4 as cf
from connectfour.gui.defines import *

class Game(Scene):
    def activate(self):
        super().activate()

        self.semaphore_chosing_move = Semaphore()

        self.start_game_setup()
    
    def on_draw(self):
        super().on_draw()
        self.draw_grid()

        if self.chosing:
            arcade.draw_circle_filled(self.position_x, PICK_ROW, RADIUS, self.color)
    
    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)
        self.position_x = x
        for column in range(fd.Field.FIELD_LENGTH):
            center = (column + 1) * MARGIN + column * 2 * RADIUS + RADIUS
            left = center - RADIUS
            right = center + RADIUS
            if x > left and x < right:
                self.position_x = center
    
    def on_mouse_release(self, x, y, dx, dy):
        super().on_mouse_release(x, y, dx, dy)
        self.move = self.get_pick_from_position()
        self.field.makeMove(self.move, self.player_color)
        self.chosing = False
        self.semaphore_chosing_move.release()
    
    def set_player_functions(self, red_player_function=None, yellow_player_function=None):
        if not red_player_function == None:
            self.player = red_player_function(self)
        if not yellow_player_function == None:
            self.oplayer = yellow_player_function(self)
    
    def start_game_setup(self):
        self.semaphore_chosing_move.acquire() # Needs to be acquired, before the start of the game

        self.window.set_mouse_visible(False)

        self.position_x = 50

        self.field = fd.Field()

        self.chosing = False
        
        self.color = arcade.color.BLACK

        game = cf(self.player, self.oplayer)
        t = Thread(target=game.play)
        t.daemon = True
        t.start()

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
    
    def get_pick_from_position(self):
        column = 0

        x = self.position_x
        while x > (MARGIN + RADIUS):
            column += 1
            x -= (2 * RADIUS + MARGIN)
        
        return column

    def make_move(self, field, color):
        self.field = field
        self.player_color = color
        if color == fd.Field.RED_PLAYER:
            self.color = arcade.color.RED
        else:
            self.color = arcade.color.YELLOW
        self.chosing = True

        self.semaphore_chosing_move.acquire()
        self.chosing = False
        
        return self.move
    
    def lost(self, field, color):
        if color == fd.Field.RED_PLAYER:
            color = fd.Field.YELLOW_PLAYER
        else:
            color = fd.Field.RED_PLAYER
        self.game_finished(color, field)
    
    def won(self, field, color):
        self.game_finished(color, field)

    def draw(self, field, color):
        self.game_finished(fd.Field.NO_PLAYER, field)
    
    def game_finished(self, winner, field):
        self.window.set_mouse_visible(True)

        self.window.switch_to_game_over_scene(field, winner)
