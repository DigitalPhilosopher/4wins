import arcade, queue, threading
import connectfour.Field as fd
import connectfour.Connect4 as cf
from connectfour.player.Connect4Player import Connect4Player as c4p

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

sem = threading.Semaphore()


class HumanPlayer(c4p):
    def __init__(self, function_holder):
        super(HumanPlayer, self).__init__()

        self.function_holder = function_holder

    def makeMove(self, field):
        return self.function_holder.make_move(field, self.color)
    
    def won(self, field):
        self.function_holder.won(field, self.color)

    def lost(self, field):
        self.function_holder.lost(field, self.color)
    
    def draw(self, field):
        self.function_holder.draw(field, self.color)



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


class ToMenuTextButton(TextButton):
    def __init__(self, center_x, center_y, action_caller):
        super().__init__(center_x, center_y, 150, 40, "Menu", 18, "Arial")
        self.action_caller = action_caller

    def on_release(self):
        super().on_release()
        self.action_caller.to_menu()



class ConnectFour(arcade.Window):
    
    def __init__(self, width, height):

        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLUE)

        self.game_over_button_list = []

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

        self.start_game_setup()
    

    def to_menu(self):
        sem.release()
        self.current_state = MENU
    

    def restart(self):
        sem.release()
        self.start_game_setup()
    

    def start_game_setup(self):
        sem.acquire() # Needs to be acquired, before the start of the game

        self.set_mouse_visible(False)

        self.position_x = 50

        self.field = fd.Field()

        self.player = HumanPlayer(self)
        self.oplayer = HumanPlayer(self)

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


    def on_mouse_press(self, x, y, dx, dy):
        if self.current_state == GAME_OVER:
            self.on_mouse_press_game_over(x, y, dx, dy)


    def on_mouse_press_game_over(self, x, y, button, key_modifiers):
        self.check_mouse_press_for_buttons(x, y, self.game_over_button_list)


    def on_mouse_release_game_over(self, x, y, button, key_modifiers):
        self.check_mouse_release_for_buttons(x, y, self.game_over_button_list)
    
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
        sem.release()
        



def main():
    ConnectFour(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()



if __name__ == "__main__":
    main()
