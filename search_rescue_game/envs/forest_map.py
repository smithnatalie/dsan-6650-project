import random
import numpy as np
from typing import Dict, List, Tuple

#Class for individual game spaces
class Cell:
    #if a north wall, need a south wall, if a west wall, need an east wall and etc.
    wall_matches: Dict[str, str] = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        
        #make sure walls exist
        self.walls: Dict[str, bool]  = {'N': True, 'S': True, 'E': True, 'W': True}
    
    #boolean to check for walls - basically to actually build this environment need to start with all walls
    def all_walls(self) -> bool:
        return all(self.walls.values())
    
    #removes walls between cells (the self space and other space) to allow  movement
    def remove_wall(self, other: 'Cell', direction: str):   
        self.walls[direction] = False
        #i.e. if not a N/S or E/W pair, shouldn't be wall unless dead end
        other.walls[Cell.wall_matches[direction]] = False
        
        
        
        

#Class for overall maps and map attributes   
class Maps:
    #how to move in each direction
    compass: Dict[str, Tuple[int, int]] = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
    
    def __init__(self, map_size: Tuple[int, int] = (10,10), map_file_path: str = None):
        self.nx: int = map_size[0]
        self.ny: int = map_size[1]
        
        #initializing all cells 
        self.cells: List[List['Cell']] = [[Cell(x, y) for y in range(self.ny)] for x in range(self.nx)]
        
        if map_file_path:
            self.load(map_file_path)
        else:
            #generating map if none at the path - may remove this if map generation is too complicated
            self.generate_map()
    
    #can pinpoint cells by coordiante
    def current_cell_object(self, x:int, y:int) -> 'Cell':
        return self.cells[x][y]
    
    #want list of neighboring cells that dog has not visited yet
    def find_new_neighbors(self, cell: 'Cell') -> List[Tuple[str,Cell]]:
        neighbors = []
        
        for direction, (dx, dy) in Maps.compass.items():
            x2, y2, = cell.x + dx, cell.y + dy
            if 0 <= x2 < self.nx and 0 <= y2 < self.ny:
                neighbor = self.current_cell_object(x2, y2)
                if neighbor.all_walls():
                    neighbors.append((direction, neighbor))
        return neighbors
    
    
    #again, may not use this but want option to generate a unique map that isn't just typing 0s and 1s into array
    # source for the recommended depth first search algorithm
    # https://medium.com/@nacerkroudir/randomized-depth-first-search-algorithm-for-maze-generation-fb2d83702742
        # not exactly the same but used cell stack code outlined in article
    def generate_map(self):
        current_cell: 'Cell' = self.cell_at(0, 0)
        cell_stack: List['Cell'] = [current_cell]

        while cell_stack:
            #get cell from stack and make it curret
            current_cell = cell_stack.pop()
            unvisited_neighbors: List[Tuple[str, Cell]] = self.find_new_neighbors(current_cell)

            if unvisited_neighbors:
                #current cell to stack
                cell_stack.append(current_cell)
                #choose unvisted neighbor randomly
                wall_direction, next_cell = random.choice(unvisited_neighbors)
                #remove existing wall between current cell and neighbor going to visit
                current_cell.remove_wall(next_cell, wall_direction)
                #now cell is visited, append to the stack
                cell_stack.append(next_cell)
                
    
    def save_map(self, map_file_path: str):
        np_cells: np.ndarray = np.zeros((self.nx, self.ny), dtype=int)

        for x in range(self.nx):
            for y in range(self.ny):
                for i, direction in enumerate(self.compass.keys()):
                    if self.cells[x][y].walls[direction]:
                        np_cells[x][y] |= 2 ** i
        #source: https://numpy.org/devdocs/reference/generated/numpy.load.html
        np.save(map_file_path, np_cells, allow_pickle=False, fix_imports=True)
    
    #for previously generated maps 
    def load_map(self, map_file_path: str):
        np_cells: np.ndarray = np.load(map_file_path, allow_pickle=False, fix_imports=True)

        for x in range(self.nx):
            for y in range(self.ny):
                for i, direction in enumerate(self.compass.keys()):
                    if np_cells[x, y] & 2 ** i == 0:
                        self.cells[x][y].walls[direction] = False
                        
                        
                        
                        
                        
        