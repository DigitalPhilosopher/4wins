import arcade
from connectfour.gui.defines import *

class TextField:
    def __init__(self,
                 text: str,
                 start_x: float, start_y: float,
                 color,
                 font_size: float=12,
                 width: int=2000,
                 align="left",
                 font_name=('Calibri', 'Arial'),
                 bold: bool=False,
                 italic: bool=False,
                 anchor_x="left",
                 anchor_y="baseline",
                 rotation=0
                ):
        self.text = text
        self.start_x = start_x
        self.start_y = start_y
        self.color = color
        self.font_size = font_size
        self.width = width
        self.align = align
        self.font_name = font_name
        self.bold = bold
        self.italic = italic
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.rotation = rotation
    
    def draw(self):
        arcade.draw_text(self.text,
                         self.start_x,
                         self.start_y,
                         self.color,
                         self.font_size,
                         self.width,
                         self.align,
                         self.font_name,
                         self.bold,
                         self.italic,
                         self.anchor_x,
                         self.anchor_y,
                         self.rotation
                        )

def create_menu_text_list():
    text_list = []

    screen_height_center = SCREEN_HEIGHT / 2
    screen_width_center = SCREEN_WIDTH / 2

    menu_text_font_size = 40
    menu_text_width = 350
    menu_start_x = screen_width_center - (menu_text_width / 2)
    menu_start_y = screen_height_center + 150

    text_list.append(TextField(MENU_TEXT, menu_start_x, menu_start_y, arcade.color.BLACK, menu_text_font_size, menu_text_width, "center"))

    player_text_font_size = 12
    player_text_width = 150
    player_text_start_x = MARGIN
    red_player_start_y = screen_height_center + 75
    yellow_player_start_y = screen_height_center - 25

    text_list.append(TextField("Red player:", player_text_start_x, red_player_start_y, arcade.color.BLACK, player_text_font_size, player_text_width, "left"))
    text_list.append(TextField("Yellow player:", player_text_start_x, yellow_player_start_y, arcade.color.BLACK, player_text_font_size, player_text_width, "left"))

    return text_list

def create_game_over_text_list(winning_player):
    text_list = []

    screen_height_center = SCREEN_HEIGHT / 2
    screen_width_center = SCREEN_WIDTH / 2

    text_width = 350
    text_start_x = screen_width_center - (text_width / 2)

    game_over_text_start_y = SCREEN_HEIGHT / 2 + 75
    game_over_text_font_size = 40

    winner_text_start_y = screen_height_center
    winner_text_font_size = 24
    winning_player_text = "WINNER: " + winning_player
    
    text_list.append(TextField(GAME_OVER_TEXT, text_start_x, game_over_text_start_y, arcade.color.BLACK, game_over_text_font_size, text_width, "center"))
    text_list.append(TextField(winning_player_text, text_start_x, winner_text_start_y, arcade.color.BLACK, winner_text_font_size, text_width, "center"))

    return text_list