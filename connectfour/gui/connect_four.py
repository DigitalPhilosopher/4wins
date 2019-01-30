import arcade, queue, threading
import connectfour.Field as fd
import connectfour.Connect4 as cf

from connectfour.gui.buttons import *
from connectfour.gui.players import *

MARGIN = 15
RADIUS = 25

SCREEN_WIDTH = (2 * RADIUS + MARGIN) * fd.Field.FIELD_LENGTH + MARGIN
SCREEN_HEIGHT = (2 * RADIUS + MARGIN) * (fd.Field.FIELD_HEIGHT + 1) + MARGIN
PICK_ROW = (2 * RADIUS + MARGIN) * fd.Field.FIELD_HEIGHT + MARGIN + RADIUS

PLAYING = 0
GAME_OVER = 1
MENU = 2

RED_PLAYER_NAME = "RED"
YELLOW_PLAYER_NAME = "YELLOW"
DRAW_PLAYER_NAME = "-"
GAME_OVER_TEXT = "GAME OVER"
MENU_TEXT = "MENU"

sem = threading.Semaphore()



class ConnectFour(arcade.Window):
    
    def __init__(self, width, height):

        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLUE)

        self.game_over_button_list = []
        self.menu_button_list = []

        width = 150
        start_y = SCREEN_HEIGHT / 2 - 50
        start_x = SCREEN_WIDTH / 2 - (width / 2 + 10)
        restart_button = RestartTextButton(start_x, start_y, self)
        self.game_over_button_list.append(restart_button)

        width = 150
        start_y = SCREEN_HEIGHT / 2 - 50
        start_x = SCREEN_WIDTH / 2 + (width / 2 + 10)
        to_menu_button = ToMenuTextButton(start_x, start_y, self)
        self.game_over_button_list.append(to_menu_button)

        width = 100
        start_y = SCREEN_HEIGHT / 2 + 40
        start_x = SCREEN_WIDTH / 2 - (width * 1.5)
        red_player_human_button = ChoosePlayerTextButton(start_x, start_y, self, fd.Field.RED_PLAYER, HumanPlayer(self), "Human")
        self.menu_button_list.append(red_player_human_button)

        width = 100
        start_y = SCREEN_HEIGHT / 2 + 40
        start_x = SCREEN_WIDTH / 2
        red_player_alphabeta_button = ChoosePlayerTextButton(start_x, start_y, self, fd.Field.RED_PLAYER, AlphaBetaPlayer(self), "AlphaBeta")
        self.menu_button_list.append(red_player_alphabeta_button)

        width = 100
        start_y = SCREEN_HEIGHT / 2 + 40
        start_x = SCREEN_WIDTH / 2 + (width * 1.5)
        red_player_minimax_button = ChoosePlayerTextButton(start_x, start_y, self, fd.Field.RED_PLAYER, MiniMaxPlayer(self), "MiniMax")
        self.menu_button_list.append(red_player_minimax_button)

        width = 100
        start_y = SCREEN_HEIGHT / 2 - 60
        start_x = SCREEN_WIDTH / 2 - (width * 1.5)
        yellow_player_human_button = ChoosePlayerTextButton(start_x, start_y, self, fd.Field.YELLOW_PLAYER, HumanPlayer(self), "Human")
        self.menu_button_list.append(yellow_player_human_button)

        width = 100
        start_y = SCREEN_HEIGHT / 2 - 60
        start_x = SCREEN_WIDTH / 2
        yellow_player_alphabeta_button = ChoosePlayerTextButton(start_x, start_y, self, fd.Field.YELLOW_PLAYER, AlphaBetaPlayer(self), "AlphaBeta")
        self.menu_button_list.append(yellow_player_alphabeta_button)

        width = 100
        start_y = SCREEN_HEIGHT / 2 - 60
        start_x = SCREEN_WIDTH / 2 + (width * 1.5)
        yellow_player_minimax_button = ChoosePlayerTextButton(start_x, start_y, self, fd.Field.YELLOW_PLAYER, MiniMaxPlayer(self), "MiniMax")
        self.menu_button_list.append(yellow_player_minimax_button)

        start_y = SCREEN_HEIGHT / 2 - 150
        start_x = SCREEN_WIDTH / 2
        start_button = StartTextButton(start_x, start_y, self)
        self.menu_button_list.append(start_button)

        yellow_player_human_button.on_press()
        yellow_player_human_button.on_release()
        red_player_human_button.on_press()
        red_player_human_button.on_release()
        self.current_state = MENU
    

    def to_menu(self):
        sem.release()
        self.current_state = MENU
    

    def restart(self):
        sem.release()
        self.start_game_setup()
    

    def start(self):
        self.start_game_setup()
    

    def start_game_setup(self):
        sem.acquire() # Needs to be acquired, before the start of the game

        self.set_mouse_visible(False)

        self.position_x = 50

        self.field = fd.Field()

        self.player = self.red_player_function
        self.oplayer = self.yellow_player_function

        self.chosing = False
        
        self.color = arcade.color.BLACK
        
        self.current_state = PLAYING

        game = cf(self.player, self.oplayer)
        t = threading.Thread(target=game.play)
        t.daemon = True
        t.start()

    
    def lost(self, field, color):
        self.field = field
        self.current_state = GAME_OVER
        self.set_mouse_visible(True)
        if color == fd.Field.RED_PLAYER:
            self.winning_player = YELLOW_PLAYER_NAME
        else:
            self.winning_player = RED_PLAYER_NAME

    
    def won(self, field, color):
        self.field = field
        self.current_state = GAME_OVER
        self.set_mouse_visible(True)
        if color == fd.Field.RED_PLAYER:
            self.winning_player = RED_PLAYER_NAME
        else:
            self.winning_player = YELLOW_PLAYER_NAME

    
    def draw(self, field, color):
        self.field = field
        self.current_state = GAME_OVER
        self.set_mouse_visible(True)
        self.winning_player = DRAW_PLAYER_NAME


    def make_move(self, field, color):
        self.field = field
        self.player_color = color
        if color == fd.Field.RED_PLAYER:
            self.color = arcade.color.RED
        else:
            self.color = arcade.color.YELLOW
        self.chosing = True

        sem.acquire()
        self.chosing = False
        ret = self.move
        
        return ret


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

        winning_player_text = "WINNER: " + self.winning_player
        width = 350
        start_y = SCREEN_HEIGHT / 2 + 75
        start_x = SCREEN_WIDTH / 2 - width / 2
        arcade.draw_text(GAME_OVER_TEXT, start_x, start_y, arcade.color.BLACK, 40, width=width, align="center")
        width = 350
        start_y = SCREEN_HEIGHT / 2
        start_x = SCREEN_WIDTH / 2 - width / 2
        arcade.draw_text(winning_player_text, start_x, start_y, arcade.color.BLACK, 24, width=width, align="center")
    
    def draw_menu(self):
        arcade.start_render()

        for button in self.menu_button_list:
            button.draw()

        width = 350
        start_y = SCREEN_HEIGHT / 2 + 150
        start_x = SCREEN_WIDTH / 2 - width / 2
        arcade.draw_text(MENU_TEXT, start_x, start_y, arcade.color.BLACK, 40, width=width, align="center")

        width = 150
        start_y = SCREEN_HEIGHT / 2 + 75
        start_x = MARGIN
        arcade.draw_text("Red player:", start_x, start_y, arcade.color.BLACK, 12, width=width, align="left")
        
        width = 150
        start_y = SCREEN_HEIGHT / 2 - 25
        start_x = MARGIN
        arcade.draw_text("Yellow player:", start_x, start_y, arcade.color.BLACK, 12, width=width, align="left")
    

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
        self.turn_off_pressed_buttons_with_color(self.menu_button_list, button, color)
        if color == fd.Field.RED_PLAYER:
            self.red_player_function = player_function
            self.red_pressed_button = button
        else:
            self.yellow_player_function = player_function
            self.yellow_pressed_button = button


    def on_mouse_press_game_over(self, x, y, button, key_modifiers):
        self.check_mouse_press_for_buttons(x, y, self.game_over_button_list)


    def on_mouse_release_game_over(self, x, y, button, key_modifiers):
        self.check_mouse_release_for_buttons(x, y, self.game_over_button_list)


    def on_mouse_press_menu(self, x, y, button, key_modifiers):
        self.check_mouse_press_for_buttons(x, y, self.menu_button_list)


    def on_mouse_release_menu(self, x, y, button, key_modifiers):
        self.check_mouse_release_for_buttons(x, y, self.menu_button_list)
    
    def turn_off_pressed_buttons_with_color(self, button_list, pressed_button, color):
        for button in button_list:
            if type(button) == ChoosePlayerTextButton and color == button.color and not button == pressed_button:
                button.turn_off_pressed()
    
    def check_mouse_press_for_buttons(self, x, y, button_list):
        for button in button_list:
            if x > button.center_x + button.width / 2:
                continue
            if x < button.center_x - button.width / 2:
                continue
            if y > button.center_y + button.height / 2:
                continue
            if y < button.center_y - button.height / 2:
                continue
            button.on_press()


    def check_mouse_release_for_buttons(self, x, y, button_list):
        for button in button_list:
            if button.pressed:
                button.on_release()

    def on_mouse_release_playing(self, x, y, dx, dy):
        self.move = self.get_pick_from_position()
        self.field.makeMove(self.move, self.player_color)
        self.chosing = False
        sem.release()
        



def main():
    ConnectFour(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()



if __name__ == "__main__":
    main()
