import arcade
import connectfour.Field as fd
from connectfour.gui.defines import *
from connectfour.gui.players import *

class TextButton:
    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.BABY_BLUE,
                 highlight_color=arcade.color.BLACK,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False


class RestartTextButton(TextButton):
    def __init__(self, center_x, center_y, action_caller):
        super().__init__(center_x, center_y, 150, 40, "Restart", 18, "Arial")
        self.action_caller = action_caller

    def on_release(self):
        super().on_release()
        self.action_caller.restart()


class StartTextButton(TextButton):
    def __init__(self, center_x, center_y, action_caller):
        super().__init__(center_x, center_y, 150, 40, "Start Game", 18, "Arial")
        self.action_caller = action_caller

    def on_release(self):
        super().on_release()
        self.action_caller.start()


class ToMenuTextButton(TextButton):
    def __init__(self, center_x, center_y, action_caller):
        super().__init__(center_x, center_y, 150, 40, "Menu", 18, "Arial")
        self.action_caller = action_caller

    def on_release(self):
        super().on_release()
        self.action_caller.to_menu()


class ChoosePlayerTextButton(TextButton):
    def __init__(self, center_x, center_y, action_caller, color, player_function, text):
        super().__init__(center_x, center_y, 125, 40, text, 18, "Arial")
        self.action_caller = action_caller
        self.color = color
        self.player_function = player_function

    def on_release(self):
        super().on_release()
        if self.color == fd.Field.RED_PLAYER:
            self.face_color = arcade.color.RED
        else:
            self.face_color = arcade.color.YELLOW
        self.action_caller.set_player(self.color, self.player_function, self)
    
    def turn_off_pressed(self):
        self.face_color = arcade.color.BABY_BLUE


def create_menu_button_list(game):
    menu_button_list = []

    menu_button_list = addStartButton(menu_button_list, game)
    menu_button_list = addRedPlayerButtons(menu_button_list, game)
    menu_button_list = addYellowPlayerButtons(menu_button_list, game)

    return menu_button_list

def addStartButton(button_list, game):
    start_y = SCREEN_HEIGHT / 2 - 150
    start_x = SCREEN_WIDTH / 2
    start_button = StartTextButton(start_x, start_y, game)
    button_list.append(start_button)

    return button_list

def addRedPlayerButtons(button_list, game):
    y_button_position = SCREEN_HEIGHT / 2 + 40
    return addPlayerButtons(button_list, game, y_button_position, fd.Field.RED_PLAYER)


def addYellowPlayerButtons(button_list, game):
    y_button_position = SCREEN_HEIGHT / 2 - 60
    return addPlayerButtons(button_list, game, y_button_position, fd.Field.YELLOW_PLAYER)

def addPlayerButtons(button_list, game, y_button_position, color):
    button_width = 100
    x_button_position_center = SCREEN_WIDTH / 2
    x_button_position_left = x_button_position_center - (button_width * 1.5)
    x_button_position_right = x_button_position_center + (button_width * 1.5)

    player_human_button = ChoosePlayerTextButton(x_button_position_left, y_button_position, game, color, HumanPlayer, "Human")
    button_list.append(player_human_button)

    player_alphabeta_button = ChoosePlayerTextButton(x_button_position_center, y_button_position, game, color, AlphaBetaPlayer, "AlphaBeta")
    button_list.append(player_alphabeta_button)

    player_minimax_button = ChoosePlayerTextButton(x_button_position_right, y_button_position, game, color, MiniMaxPlayer, "MiniMax")
    button_list.append(player_minimax_button)
    
    player_human_button.on_press()
    player_human_button.on_release()

    return button_list


def create_game_over_button_list(game):
    button_list = []

    button_list.append(create_restart_button(game))
    button_list.append(create_menu_button(game))

    return button_list

def create_restart_button(game):
    (x_button_position_left, _, y_button_position) = calculate_game_over_button_positions()
    return RestartTextButton(x_button_position_left, y_button_position, game)

def create_menu_button(game):
    (_, x_button_position_right, y_button_position) = calculate_game_over_button_positions()
    return ToMenuTextButton(x_button_position_right, y_button_position, game)

def calculate_game_over_button_positions():
    button_width = 150
    x_button_position_center = SCREEN_WIDTH / 2
    x_button_position_left = x_button_position_center - (button_width / 2 + 10)
    x_button_position_right = x_button_position_center + (button_width / 2 + 10)
    y_button_position = SCREEN_HEIGHT / 2 - 50

    return (x_button_position_left, x_button_position_right, y_button_position)

def turn_off_pressed_buttons_with_color(button_list, pressed_button, color):
    for button in button_list:
        if is_button_to_turn_off(button, pressed_button, color):
            button.turn_off_pressed()

def is_button_to_turn_off(button, pressed_button, color):
    return type(button) == ChoosePlayerTextButton and color == button.color and not button == pressed_button

def check_mouse_press_for_buttons(x, y, button_list):
    for button in button_list:
        if point_is_in_button(x, y, button):
            button.on_press()

def point_is_in_button(x, y, button):
    if x > button.center_x + button.width / 2:
        return False
    if x < button.center_x - button.width / 2:
        return False
    if y > button.center_y + button.height / 2:
        return False
    if y < button.center_y - button.height / 2:
        return False
    return True


def check_mouse_release_for_buttons(x, y, button_list):
    for button in button_list:
        if button.pressed:
            button.on_release()