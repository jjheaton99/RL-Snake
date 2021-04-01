import arcade

from snake_game_view import SnakeGameView

if __name__ == "__main__":
    window = arcade.Window(600, 600, 'Snek')
    game_view = SnakeGameView(grid_size=(25, 25))
    window.show_view(game_view)
    arcade.run()