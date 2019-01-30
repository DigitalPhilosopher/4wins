import arcade
import connectfour.Field as fd

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