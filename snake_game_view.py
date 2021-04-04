import arcade
import numpy as np

from snake_game_logic import SnakeGameLogic

import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')

from tensorforce.agents import Agent
import train_agent

class SnakeGameView(arcade.View):
    """
    Implementation of the snake game logic using Arcade, including
    option to let trained DQN agent take over.
    """
    def __init__(self, grid_size=(20, 20), network_type='dense'):
        super().__init__()
        self.grid_size = grid_size
        self.network_type = network_type
        
        self.square_size = 30
        self.w_width = (grid_size[1] + 2) * self.square_size 
        self.w_height = (grid_size[0] + 2) * self.square_size
        self.window.set_size(self.w_width, self.w_height)
        
        self.snake_game_logic = SnakeGameLogic(grid_size)
        self.update_timestep = 0.1
        
        if network_type == 'dense':
            self.agent = Agent.load(directory='agents/dense',
                                    filename='dqn_agent',
                                    environment=train_agent.dense_env,
                                    **train_agent.dense_config)
            
        elif network_type == 'conv':
            self.agent = Agent.load(directory='agents/conv',
                                    filename='dqn_agent',
                                    environment=train_agent.conv_env,
                                    **train_agent.conv_config)
            
        elif network_type == 'multi':
            self.agent = Agent.load(directory='agents/multi_ddqn',
                                    filename='dqn_agent',
                                    environment=train_agent.multi_env,
                                    **train_agent.multi_config)
            
        else:
            raise Exception('Invalid network type.')
        
        self.setup()
        
        arcade.set_background_color(arcade.color.BLACK)
        
    def setup(self):
        self.snake_game_logic.reset()
        self.cumulative_time = 0.0
        self.game_started = False
        self.agent_playing = False
        return
        
    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_rectangle_filled(
            self.w_width / 2, 
            self.w_height / 2, 
            self.w_width - 2 * self.square_size, 
            self.w_height - 2 * self.square_size, 
            arcade.color.SKY_BLUE)
        
        head = True
        colour_counter = 1
        colour_factor = 255 / (self.snake_game_logic.score + 3)
        for coord in self.snake_game_logic.snake_coords:
            if head:
                head = False
                arcade.draw_rectangle_filled(
                    (coord[1] + 1) * self.square_size + self.square_size / 2.0, 
                    self.w_height - (coord[0] + 1) * self.square_size - self.square_size / 2.0, 
                    self.square_size, 
                    self.square_size, 
                    (255, 0, 0))
            else:
                arcade.draw_rectangle_filled(
                    (coord[1] + 1) * self.square_size + self.square_size / 2.0, 
                    self.w_height - (coord[0] + 1) * self.square_size - self.square_size / 2.0, 
                    self.square_size, 
                    self.square_size, 
                    (255 - colour_factor * colour_counter, 0, 0))
                colour_counter += 1
        
        food_coord = self.snake_game_logic.food_coord
        arcade.draw_rectangle_filled(
            (food_coord[1] + 1) * self.square_size + self.square_size / 2.0, 
            self.w_height - (food_coord[0] + 1) * self.square_size - self.square_size / 2.0, 
            self.square_size, 
            self.square_size, 
            arcade.color.BANGLADESH_GREEN)
        
        arcade.draw_text(
            'Score: {}'.format(self.snake_game_logic.score), 
            self.w_width / 2, 
            self.square_size / 2,
            arcade.color.WHITE,
            font_size=20,
            align="center",
            anchor_x="center", 
            anchor_y="center")
        
        if self.snake_game_logic.lose:
            arcade.draw_text(
                'Game over!', 
                self.w_width / 2, 
                self.w_height - self.square_size / 2,
                arcade.color.WHITE,
                font_size=20,
                align="center",
                anchor_x="center", 
                anchor_y="center")

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
            
        if symbol == arcade.key.L and self.game_started:
            self.update_timestep *= 0.9
            
        if symbol == arcade.key.J and self.game_started:
            self.update_timestep /= 0.9
            
        if symbol == arcade.key.K:
            self.update_timestep = 0.1
        
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

    def on_update(self, delta_time):
        if self.game_started:
            self.cumulative_time += delta_time
            while self.cumulative_time > self.update_timestep:
                self.cumulative_time -= self.update_timestep
                if self.agent_playing:
                    action = self.agent.act(self.snake_game_logic.get_state(self.network_type))
                    self.snake_game_logic.change_direction(action)
                    self.agent.observe()
                self.snake_game_logic.update()