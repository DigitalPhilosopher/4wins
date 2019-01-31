import arcade, queue, threading
import connectfour.Field as fd
import connectfour.Connect4 as cf

from connectfour.gui.buttons import *
from connectfour.gui.texts import *
from connectfour.gui.players import *
from connectfour.gui.defines import *

class ConnectFour(arcade.Window):
    
    def __init__(self, width, height):
        super().__init__(width, height)

        self.semaphore_chosing_move = threading.Semaphore()

        arcade.set_background_color(arcade.color.BLUE)

        self.create_buttons()
        self.create_texts()

        self.current_state = MENU
    
    def create_texts(self):
        self.menu_text_list = create_menu_text_list()
        self.game_over_text_list = create_game_over_text_list(DRAW_PLAYER_NAME)
    
    def create_buttons(self):
        self.menu_button_list = []
        self.menu_button_list = create_menu_button_list(self)
        self.game_over_button_list = create_game_over_button_list(self)
    

    def to_menu(self):
        self.semaphore_chosing_move.release()
        self.current_state = MENU
    

    def restart(self):
        self.semaphore_chosing_move.release()
        self.start_game_setup()
    

    def start(self):
        self.start_game_setup()
    

    def start_game_setup(self):
        self.semaphore_chosing_move.acquire() # Needs to be acquired, before the start of the game

        self.set_mouse_visible(False)

        self.position_x = 50

        self.field = fd.Field()

        self.player = self.red_player_function(self)
        self.oplayer = self.yellow_player_function(self)

        self.chosing = False
        
        self.color = arcade.color.BLACK
        
        self.current_state = PLAYING

        game = cf(self.player, self.oplayer)
        t = threading.Thread(target=game.play)
        t.daemon = True
        t.start()

    
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
        self.set_mouse_visible(True)

        self.field = field
        self.current_state = GAME_OVER
        self.set_winner_text(winner)

    def set_winner_text(self, color):
        if color == fd.Field.RED_PLAYER:
            self.game_over_text_list = create_game_over_text_list(RED_PLAYER_NAME)
        elif color == fd.Field.YELLOW_PLAYER:
            self.game_over_text_list = create_game_over_text_list(YELLOW_PLAYER_NAME)
        else:
            self.game_over_text_list = create_game_over_text_list(DRAW_PLAYER_NAME)


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


    def on_draw(self):
        if self.current_state == PLAYING:
            self.draw_playing()
        elif self.current_state == GAME_OVER:
            self.draw_gameover()
        elif self.current_state == MENU:
            self.draw_menu()


    def draw_gameover(self):
        arcade.start_render()

        self.draw_grid()

        for button in self.game_over_button_list:
            button.draw()
        
        for text in self.game_over_text_list:
            text.draw()
    
    def draw_menu(self):
        arcade.start_render()

        for button in self.menu_button_list:
            button.draw()
        
        for text in self.menu_text_list:
            text.draw()
    

    def draw_playing(self):
        arcade.start_render()

        self.draw_grid()

        if self.chosing:
            arcade.draw_circle_filled(self.position_x, PICK_ROW, RADIUS, self.color)
    

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
        if self.current_state == PLAYING:
            self.on_mouse_motion_playing(x, y, dx, dy)
    

    def on_mouse_motion_playing(self, x, y, dx, dy):
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
        if self.current_state == PLAYING:
            self.on_mouse_release_playing(x, y, dx, dy)
        elif self.current_state == GAME_OVER:
            self.on_mouse_release_game_over(x, y, dx, dy)
        elif self.current_state == MENU:
            self.on_mouse_release_menu(x, y, dx, dy)


    def on_mouse_press(self, x, y, dx, dy):
        if self.current_state == GAME_OVER:
            self.on_mouse_press_game_over(x, y, dx, dy)
        elif self.current_state == MENU:
            self.on_mouse_press_menu(x, y, dx, dy)

    
    def set_player(self, color, player_function, button):
        turn_off_pressed_buttons_with_color(self.menu_button_list, button, color)
        if color == fd.Field.RED_PLAYER:
            self.red_player_function = player_function
            self.red_pressed_button = button
        else:
            self.yellow_player_function = player_function
            self.yellow_pressed_button = button


    def on_mouse_press_game_over(self, x, y, button, key_modifiers):
        check_mouse_press_for_buttons(x, y, self.game_over_button_list)


    def on_mouse_release_game_over(self, x, y, button, key_modifiers):
        check_mouse_release_for_buttons(x, y, self.game_over_button_list)


    def on_mouse_press_menu(self, x, y, button, key_modifiers):
        check_mouse_press_for_buttons(x, y, self.menu_button_list)


    def on_mouse_release_menu(self, x, y, button, key_modifiers):
        check_mouse_release_for_buttons(x, y, self.menu_button_list)

    def on_mouse_release_playing(self, x, y, dx, dy):
        self.move = self.get_pick_from_position()
        self.field.makeMove(self.move, self.player_color)
        self.chosing = False
        self.semaphore_chosing_move.release()
        



def main():
    ConnectFour(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()



if __name__ == "__main__":
    main()
