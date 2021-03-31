import arcade
import numpy as np

from tfe_logic import TFELogic

class SnakeGameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.win_width, self.win_height = self.window.get_size()
        arcade.set_background_color(arcade.color.SKY_BLUE)
        
    def setup(self):
        return
        
    def on_draw(self):
        arcade.start_render()

    def on_key_press(self, symbol, modifiers):      
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

    def on_update(self, delta_time):
        self.win_width, self.win_height = self.window.get_size()