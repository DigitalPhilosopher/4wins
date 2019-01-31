from connectfour.gui.scene import Scene
from connectfour.gui.defines import *
from connectfour.gui.buttons import *
from connectfour.gui.texts import *


class GameOver(Scene):
    def __init__(self, window):
        super(GameOver, self).__init__(window)

        self.winner = DRAW_PLAYER_NAME

        self.create_texts()
        self.create_buttons()
    
    def on_draw(self):
        super().on_draw()

        self.draw_grid()

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

    def set_winner_text(self, color):
        if color == fd.Field.RED_PLAYER:
            self.winner = RED_PLAYER_NAME
        elif color == fd.Field.YELLOW_PLAYER:
            self.winner = YELLOW_PLAYER_NAME
        else:
            self.winner = DRAW_PLAYER_NAME
        
        self.create_texts()

    def set_field(self, field):
        self.field = field

    def create_texts(self):
        self.text_list = create_game_over_text_list(self.winner)
    
    def create_buttons(self):
        self.button_list = create_game_over_button_list(self)
    
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

    def restart(self):
        self.window.switch_to_game_scene()

    def to_menu(self):
        self.window.switch_to_menu_scene()
