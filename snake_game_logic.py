import numpy as np

class SnakeGameLogic:
    def __init__(self, grid_size=(20, 20)):
        self.grid_size = grid_size
        self.grid = np.zeros(grid_size)
        self.ate_food = False
        self.reset()
        
    def reset(self):
        """
        Setup grid that contains state of game, and reset snake.
        
        --Grid value key--
        0: empty space
        1: body segment
        2: snake head
        3: food
        
        Creates snake moving right with length of 3 in the middle of the grid.

        Snake is represented as a list of coordinates of body segments
        starting with the head.
        """
        self.lose = False
        self.score = 0
        self.steps_since_ate = 0
        
        #direction of motion of snake head, 0=up, 1=left, 2=down, 3=right
        self.direction = 3
        self.direction_changed = False
        
        head_start_point = np.floor_divide(np.array(self.grid_size), 2).tolist()      
        self.snake_coords = [head_start_point, 
                             [head_start_point[0], head_start_point[1] - 1], 
                             [head_start_point[0], head_start_point[1] - 2]]

        self.place_food_random()
        self.stored_grids = None
        self.update()
        self.stored_grids = [self.grid, 
                             self.grid,
                             self.grid,
                             self.grid]
        
    def move_snake(self):
        #if snake ate food, end position is kept
        if not self.ate_food:
            del self.snake_coords[-1]
        else:
            self.ate_food = False
            
        new_head_pos = self.snake_coords[0][:]
        #for boundary-less game
        """
        if self.direction == 0:
            if new_head_pos[0] == 0:
                new_head_pos[0] = self.grid_size[0] - 1
            else:
                new_head_pos[0] -= 1
        elif self.direction == 1:
            if new_head_pos[1] == 0:
                new_head_pos[1] = self.grid_size[1] - 1
            else:
                new_head_pos[1] -= 1
        elif self.direction == 2:
            if new_head_pos[0] == self.grid_size[0] - 1:
                new_head_pos[0] = 0
            else:
                new_head_pos[0] += 1
        elif self.direction == 3:
            if new_head_pos[1] == self.grid_size[1] - 1:
                new_head_pos[1] = 0
            else:
                new_head_pos[1] += 1
        """
        
        if self.direction == 0:
            if new_head_pos[0] == 0:
                return True
            else:
                new_head_pos[0] -= 1
        elif self.direction == 1:
            if new_head_pos[1] == 0:
                return True
            else:
                new_head_pos[1] -= 1
        elif self.direction == 2:
            if new_head_pos[0] == self.grid_size[0] - 1:
                return True
            else:
                new_head_pos[0] += 1
        elif self.direction == 3:
            if new_head_pos[1] == self.grid_size[1] - 1:
                return True
            else:
                new_head_pos[1] += 1
        
        #return True if snake ate itself
        for segment in self.snake_coords:
            if new_head_pos == segment:
                return True
        
        self.snake_coords.insert(0, new_head_pos)
        
        return False
        
    def get_snake_slice(self):
        #returns snake positions as tuple for slicing grid array
        #gives head position separately
        row_idxs = np.array([])
        col_idxs = np.array([])
        head = True
        for coord in self.snake_coords:
            if head:
                head_coord = tuple(coord)
                head = False
            else:
                row_idxs = np.append(row_idxs, coord[0])
                col_idxs = np.append(col_idxs, coord[1])
        return head_coord, (row_idxs.astype(int), col_idxs.astype(int))
    
    def update(self):
        if not self.lose:
            #move snake and return True if it ate istelf
            if self.move_snake():
                self.lose = True
                return True
            
            self.steps_since_ate += 1
            
            #reset grid and replace snake and food
            self.grid = np.zeros(self.grid_size)
            self.grid[tuple(self.food_coord)] = 3
            head_coord, body_coords = self.get_snake_slice()
            self.grid[head_coord] = 2
            self.grid[body_coords] = 1
             
            #check if food was eaten and if so, replace it
            if np.where(self.grid == 3)[0].size == 0:
                self.ate_food = True
                self.score += 1
                self.steps_since_ate = 0
                self.place_food_random()
            
            #allow direction change again after update
            self.direction_changed = False
            
            #update stored grid values
            if self.stored_grids is not None:
                del self.stored_grids[-1]
                self.stored_grids.insert(0, self.grid)
        return False
    
    def place_food_random(self):
        #assigns value of 3 to random empty grid position creating "food"
        zero_positions = np.where(self.grid == 0) 
        rand_idx = np.random.randint(np.size(zero_positions[0]))
        self.food_coord = [zero_positions[0][rand_idx], 
                           zero_positions[1][rand_idx]]
        self.grid[tuple(self.food_coord)] = 3
    
    def change_direction(self, direction):
        if direction == 'u':
            direction = 0
        elif direction == 'l':
            direction = 1
        elif direction == 'd':
            direction = 2
        elif direction == 'r':
            direction = 3
            
        #do not allow direction to be reversed
        if abs(self.direction - direction) == 2:
            return
        
        #ensure at least one movement is performed between direction changes
        if self.direction_changed:
            self.direction_changed = False
            return
        
        self.direction = direction
        self.direction_changed = True
        
    def distance_to_food(self):
        return np.sqrt((self.food_coord[0] - self.snake_coords[0][0])**2 + 
                       (self.food_coord[1] - self.snake_coords[0][1])**2)
        
    def get_flat_grid(self):
        return self.grid.flatten().astype('int').tolist()
    
    def get_stacked_stored_grids(self):
        return np.stack(self.stored_grids, axis=2).astype('float').tolist()
    
    def get_state_info(self):
        #direction of motion
        up = 0.0
        left = 0.0
        down = 0.0
        right = 0.0
    
        #check for immediate danger from snake body or boundary
        right_danger = 0.0
        left_danger = 0.0
        forward_danger = 0.0
        head_coord = self.snake_coords[0]
        if self.direction == 0:
            up = 1.0
            if head_coord[0] == 0:
                forward_danger = 1.0
            elif self.grid[head_coord[0] - 1, head_coord[1]] == 1:
                forward_danger = 1.0
            if head_coord[1] == 0:
                left_danger = 1.0
            elif self.grid[head_coord[0], head_coord[1] - 1] == 1:
                left_danger = 1.0
            if head_coord[1] == self.grid_size[1] - 1:
                right_danger = 1.0
            elif self.grid[head_coord[0], head_coord[1] + 1] == 1:
                right_danger = 1.0
            
        elif self.direction == 1:
            left = 1.0
            if head_coord[1] == 0:
                forward_danger = 1.0
            elif self.grid[head_coord[0], head_coord[1] - 1] == 1:
                forward_danger = 1.0
            if head_coord[0] == 0:
                right_danger = 1.0
            elif self.grid[head_coord[0] - 1, head_coord[1]] == 1:
                right_danger = 1.0
            if head_coord[0] == self.grid_size[0] - 1:
                left_danger = 1.0
            elif self.grid[head_coord[0] + 1, head_coord[1]] == 1:
                left_danger = 1.0

        elif self.direction == 2:
            down = 1.0
            if head_coord[0] == self.grid_size[0] - 1:
                forward_danger = 1.0
            elif self.grid[head_coord[0] + 1, head_coord[1]] == 1:
                forward_danger = 1.0
            if head_coord[1] == 0:
                right_danger = 1.0
            elif self.grid[head_coord[0], head_coord[1] - 1] == 1:
                right_danger = 1.0
            if head_coord[1] == self.grid_size[1] - 1:
                left_danger = 1.0
            elif self.grid[head_coord[0], head_coord[1] + 1] == 1:
                left_danger = 1.0

        elif self.direction == 3:
            right = 1.0
            if head_coord[1] == self.grid_size[1] - 1:
                forward_danger = 1.0
            elif self.grid[head_coord[0], head_coord[1] + 1] == 1:
                forward_danger = 1.0
            if head_coord[0] == 0:
                left_danger = 1.0
            elif self.grid[head_coord[0] - 1, head_coord[1]] == 1:
                left_danger = 1.0
            if head_coord[0] == self.grid_size[0] - 1:
                right_danger = 1.0
            elif self.grid[head_coord[0] + 1, head_coord[1]] == 1:
                right_danger = 1.0
        
        #check direction of food
        food_up = 0.0
        food_left = 0.0
        food_down = 0.0
        food_right = 0.0
        if self.food_coord[0] < head_coord[0]:
            food_up = 1.0
        if self.food_coord[1] < head_coord[1]:
            food_left = 1.0
        if self.food_coord[0] > head_coord[0]:
            food_down = 1.0
        if self.food_coord[1] > head_coord[1]:
            food_right = 1.0

        return [up,
                left,
                down,
                right,
                forward_danger,
                left_danger,
                right_danger,
                food_up,
                food_left,
                food_down,
                food_right]
    
    def get_state(self, network_type):
        #encodes state of the game for RL algorithm input for either dense or conv networks
        if network_type == 'dense':
            return self.get_state_info()
        
        elif network_type == 'conv':
            return np.expand_dims(self.grid.astype('float'), axis=2).tolist()
        
        elif network_type == 'multi':
            return dict(image_input=self.get_stacked_stored_grids(), 
                        info_input=self.get_state_info())
        
        else:
            raise Exception('Invalid network type.')
    
    def rl_agent_change_direction(self, direction):
        self.change_direction(direction)
        return self.update()
        
    def print(self):
        print(self.grid)