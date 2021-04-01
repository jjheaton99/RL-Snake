from tensorforce.environments import Environment

from snake_game_logic import SnakeGameLogic

class SnakeEnvironment(Environment):
    def __init__(self, grid_size=(20, 20)):
        super().__init__()
        self.grid_size = grid_size
        self.snake_game_logic = SnakeGameLogic(grid_size)
        
    def states(self):
        return dict(type='float', shape=(11,))

    def actions(self):
        return dict(type='int', num_values=4)
    
    def reset(self):
        self.snake_game_logic.reset()
        return self.snake_game_logic.get_state()
    
    def reward(self):
        reward = -0.0001
        if self.snake_game_logic.ate_food:
            reward += 10.0
        if self.snake_game_logic.lose:
            reward -= 10.0
        return reward
    
    def execute(self, actions):
        next_state, terminal = self.snake_game_logic.rl_agent_change_direction(actions)
        reward = self.reward()
        if terminal:
            print(self.snake_game_logic.score)
        return next_state, terminal, reward