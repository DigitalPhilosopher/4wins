import arcade

from connectfour.gui.defines import SCREEN_HEIGHT, SCREEN_WIDTH
from connectfour.gui.menu import Menu
from connectfour.gui.game import Game
from connectfour.gui.game_over import GameOver

class ConnectFour(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLUE)

        self.init_scenes()

    def init_scenes(self):
        self.menu_scene = Menu(self)
        self.game_scene = Game(self)
        self.game_over_scene = GameOver(self)

        self.switch_to_menu_scene()

    def switch_to_menu_scene(self):
        self.active_scene = self.menu_scene
        self.active_scene.activate()

    def switch_to_game_scene(self, red_player=None, yellow_player=None):
        self.game_scene.set_player_functions(red_player, yellow_player)

        self.active_scene = self.game_scene
        self.active_scene.activate()

    def switch_to_game_over_scene(self, field, winner):
        self.game_over_scene.set_winner_text(winner)
        self.game_over_scene.set_field(field)

        self.active_scene = self.game_over_scene
        self.active_scene.activate()

    def on_draw(self):
        arcade.start_render()
        self.active_scene.on_draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.active_scene.on_mouse_motion(x, y, dx, dy)

    def on_mouse_release(self, x, y, dx, dy):
        self.active_scene.on_mouse_release(x, y, dx, dy)

    def on_mouse_press(self, x, y, dx, dy):
        self.active_scene.on_mouse_press(x, y, dx, dy)


def main():
    ConnectFour(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()
