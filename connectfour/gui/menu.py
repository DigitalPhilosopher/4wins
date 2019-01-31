from connectfour.gui.scene import Scene
from connectfour.gui.buttons import *
from connectfour.gui.texts import *


class Menu(Scene):
    def __init__(self, window):
        super(Menu, self).__init__(window)
        self.create_texts()
        self.create_buttons()

    def on_draw(self):
        super().on_draw()

        for button in self.button_list:
            button.draw()
        
        for text in self.text_list:
            text.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        super().on_mouse_press(x, y, button, key_modifiers)
        check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        super().on_mouse_release(x, y, button, key_modifiers)
        check_mouse_release_for_buttons(x, y, self.button_list)

    def start(self):
        self.window.switch_to_game_scene(self.red_player_function, self.yellow_player_function)

    def set_player(self, color, player_function, button):
        turn_off_pressed_buttons_with_color(self.button_list, button, color)
        if color == fd.Field.RED_PLAYER:
            self.red_player_function = player_function
            self.red_pressed_button = button
        else:
            self.yellow_player_function = player_function
            self.yellow_pressed_button = button

    def create_texts(self):
        self.text_list = create_menu_text_list()

    def create_buttons(self):
        self.button_list = []
        self.button_list = create_menu_button_list(self)
