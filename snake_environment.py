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
        else:
            raise Exception('Invalid network type, should be dense or conv.')

    def actions(self):
        return dict(type='int', num_values=4)
    
    def reset(self):
        self.snake_game_logic.reset()
        return self.snake_game_logic.get_state(self.network_type)
    
    def reward(self):
        reward = 0.0
        if self.snake_game_logic.ate_food:
            reward += 1.0
        if self.snake_game_logic.lose:
            reward -= 1.0
        return reward
    
    def execute(self, actions):
        terminal = self.snake_game_logic.rl_agent_change_direction(actions)
        next_state = self.snake_game_logic.get_state(self.network_type)
        reward = self.reward()
        if terminal:
            print(self.snake_game_logic.score)
        return next_state, terminal, reward