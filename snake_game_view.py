import arcade
import numpy as np

from snake_game_logic import SnakeGameLogic

import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')

from tensorforce.agents import Agent
from snake_environment import SnakeEnvironment
environment = SnakeEnvironment()

class SnakeGameView(arcade.View):
    """
    Implementation of the snake game logic using Arcade, including
    option to let trained DQN agent take over.
    """
    def __init__(self, grid_size=(20, 20)):
        super().__init__()
        self.grid_size = grid_size
        
        self.square_size = 30
        self.w_width = grid_size[1] * self.square_size
        self.w_height = grid_size[0] * self.square_size
        self.window.set_size(self.w_width, self.w_height)
        
        self.snake_game_logic = SnakeGameLogic(grid_size)
        self.update_timestep = 0.1
        
        self.agent = Agent.load('agents',
                                'checkpoint',
                                agent='dqn',
                                batch_size=10,
                                environment=environment,
                                learning_rate=1e-3,
                                network=dict(type='auto',
                                             size=64,
                                             depth=4),
                                memory=10000,
                                saver=dict(directory='agents',
                                           frequency=10000))
        
        self.setup()
        
        arcade.set_background_color(arcade.color.SKY_BLUE)
        
    def setup(self):
        self.snake_game_logic.reset()
        self.cumulative_time = 0.0
        self.game_started = False
        self.agent_playing = False
        return
        
    def on_draw(self):
        arcade.start_render()
        
        head = True
        for coord in self.snake_game_logic.snake_coords:
            if head:
                head = False
                arcade.draw_rectangle_filled(
                    coord[1] * self.square_size + self.square_size / 2.0, 
                    self.w_height - coord[0] * self.square_size - self.square_size / 2.0, 
                    self.square_size, 
                    self.square_size, 
                    arcade.color.RED_DEVIL)
            else:
                arcade.draw_rectangle_filled(
                    coord[1] * self.square_size + self.square_size / 2.0, 
                    self.w_height - coord[0] * self.square_size - self.square_size / 2.0, 
                    self.square_size, 
                    self.square_size, 
                    arcade.color.BLACK)
        
        food_coord = self.snake_game_logic.food_coord
        arcade.draw_rectangle_filled(
            food_coord[1] * self.square_size + self.square_size / 2.0, 
            self.w_height - food_coord[0] * self.square_size - self.square_size / 2.0, 
            self.square_size, 
            self.square_size, 
            arcade.color.GREEN)

    def on_key_press(self, symbol, modifiers):    
        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.snake_game_logic.change_direction('u')
            self.game_started = True
            self.agent_playing = False 

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.snake_game_logic.change_direction('l')
            self.game_started = True
            self.agent_playing = False 

        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.snake_game_logic.change_direction('d')
            self.game_started = True
            self.agent_playing = False 

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.snake_game_logic.change_direction('r')
            self.game_started = True
            self.agent_playing = False 
              
        if symbol == arcade.key.B:
            self.game_started = True
            self.agent_playing = not self.agent_playing  
            
        if symbol == arcade.key.R:
            self.setup()  
        
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

    def on_update(self, delta_time):
        if self.game_started:
            self.cumulative_time += delta_time
            while self.cumulative_time > self.update_timestep:
                self.cumulative_time -= self.update_timestep
                if self.agent_playing:
                    action = self.agent.act(self.snake_game_logic.get_state('dense'))
                    self.snake_game_logic.change_direction(action)
                    self.agent.observe()
                self.snake_game_logic.update()