import arcade

from snake_game_view import SnakeGameView

if __name__ == "__main__":
    window = arcade.Window(800, 600, 'Snek')
    game_view = SnakeGameView()
    window.show_view(game_view)
    arcade.run()