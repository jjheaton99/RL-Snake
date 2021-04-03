from tensorforce.environments import Environment

from snake_game_logic import SnakeGameLogic

class SnakeEnvironment(Environment):
    def __init__(self, grid_size=(20, 20), network_type='dense'):
        super().__init__()
        self.grid_size = grid_size
        self.network_type = network_type
        self.snake_game_logic = SnakeGameLogic(grid_size)
        
    def states(self):
        if self.network_type == 'dense':
            return dict(type='float', shape=(11,))
        elif self.network_type == 'conv':
            return dict(type='float', shape=(self.grid_size[0], self.grid_size[1], 1))
        elif self.network_type == 'multi':
            return dict(
                    image_input=dict(type='float', shape=(self.grid_size[0], self.grid_size[1], 4)),
                    info_input=dict(type='float', shape=(11,))
                )
        else:
            raise Exception('Invalid network type.')

    def actions(self):
        return dict(type='int', num_values=4)
    
    def reset(self):
        print(self.snake_game_logic.score)
        self.snake_game_logic.reset()
        return self.snake_game_logic.get_state(self.network_type)
    
    def reward(self):
        reward = 0.0
        time_reward = 0.0
        distance_reward = 0.0
        
        if self.snake_game_logic.ate_food:
            reward += 1.0
        if self.snake_game_logic.lose:
            reward -= 1.0
        
        #punish if agent takes too long to get food, scaled inversely with snake length
        patience = 200
        if self.snake_game_logic.steps_since_ate > patience:
            time_reward = 1e-6 * (self.snake_game_logic.steps_since_ate - patience) / (self.snake_game_logic.score + 1.0)
            
        #reward for being closer to food, scaled inversely with snake length
        min_distance = 14.0
        if self.snake_game_logic.distance_to_food() < min_distance:
            distance_reward = 1e-3 / (self.snake_game_logic.distance_to_food() * (self.snake_game_logic.score + 1.0))
        
        reward = reward - time_reward + distance_reward
        
        #if time_reward > 0.0:
         #   print('dist - time: {}'.format(distance_reward - time_reward))
        
        #clip reward in range [-1, 1]
        if abs(reward) > 1.0:
            reward /= abs(reward)
        return reward
    
    def execute(self, actions):
        terminal = self.snake_game_logic.rl_agent_change_direction(actions)
        next_state = self.snake_game_logic.get_state(self.network_type)
        reward = self.reward()
        return next_state, terminal, reward