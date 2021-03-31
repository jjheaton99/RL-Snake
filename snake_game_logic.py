import numpy as np

class SnakeGameLogic:
    def __init__(self, grid_size=(20, 30)):
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
        
        #direction of motion of snake head, 1=up, 2=left, 3=down, 4=right
        self.direction = 4
        self.direction_changed = False
        
        head_start_point = np.floor_divide(np.array(self.grid_size), 2).tolist()      
        self.snake_coords = [head_start_point, 
                             [head_start_point[0], head_start_point[1] - 1], 
                             [head_start_point[0], head_start_point[1] - 2]]

        self.place_food_random()
        self.update()
        
    def move_snake(self):
        #if snake ate food, end position is kept
        if not self.ate_food:
            del self.snake_coords[-1]
        else:
            self.ate_food = False
            
        new_head_pos = self.snake_coords[0][:]
        if self.direction == 1:
            if new_head_pos[0] == 0:
                new_head_pos[0] = self.grid_size[0] - 1
            else:
                new_head_pos[0] -= 1
        elif self.direction == 2:
            if new_head_pos[1] == 0:
                new_head_pos[1] = self.grid_size[1] - 1
            else:
                new_head_pos[1] -= 1
        elif self.direction == 3:
            if new_head_pos[0] == self.grid_size[0] - 1:
                new_head_pos[0] = 0
            else:
                new_head_pos[0] += 1
        elif self.direction == 4:
            if new_head_pos[1] == self.grid_size[1] - 1:
                new_head_pos[1] = 0
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
                self.place_food_random()
            
            #allow direction change again after update
            self.direction_changed = False
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
            direction = 1
        elif direction == 'l':
            direction = 2
        elif direction == 'd':
            direction = 3
        elif direction == 'r':
            direction = 4
            
        #do not allow direction to be reversed
        if abs(self.direction - direction) == 2:
            return
        
        #ensure at least one movement is performed between direction changes
        if self.direction_changed:
            self.direction_changed = False
            return
        
        self.direction = direction
        self.direction_changed = True
        
    def print(self):
        print(self.grid)

"""
from time import sleep        

snek = SnakeGameLogic((2, 10))
for _ in range(1000):
    snek.update()
    snek.print()
    sleep(0.5)
"""