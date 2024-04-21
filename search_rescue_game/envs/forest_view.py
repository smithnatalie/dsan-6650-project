import pygame
import numpy as np
import os
import random

class ForestViews:
    #starting w 10x10
    def __init__(self, map_name = "ForestView", map_file_path=None,
                 map_size=(10, 10), screen_size=(600,600),
                 has_loops=False, num_portals=0, enable_render=True):
        
        #pygame configs
        pygame.init()
        pygame.display.set_caption(map_name)
        self.clock = pygame.time.Clock()
        self.__game_over = False
        self.__enable_render = enable_render
        
        #loading the forest map view
        if map_file_path is None:
            self.__maps = Maps(map_size=map_size, has_loops=has_loops, num_portals=num_portals)
        else:
            if not os.path.exists(map_file_path):
                dir_path = os.path.dirname(os.path.abspath(__file__))
                rel_path = os.path.join(dir_path, "map_options", map_file_path)
                #for error capturing if file not found:
                if os.path.exists(rel_path):
                    map_file_path = rel_path
                else:
                    raise FileExistsError("Unable to locate map %s." % map_file_path)
                #MAY NEED TO FIX THIS
            self.__maps = Maps(map_cells=Maps.load_map(map_file_path))
            
        self.map_size = self.__maps.map_size
        if self.__enable_render is True:
            #showing bottom right area
            self.screen = pygame.display.set_mode(screen_size)
            self.__screen_size = tuple(map(sum, zip(screen_size, (-1, -1))))
            
        #starting point - can change
        self.__beginning = np.zeros(2, dtype=int)
        
        #end goal- rescue spot - can change
        # self.__goal = np.array(self.map_size) - np.array(1,1)
        
        self.__goal = np.array(self.map_size) - np.array([1,1])
        
        #creating agent dog
        # self.__dog = self.beginning
        self.__dog = np.zeros(2, dtype=int)
        
        #debugging statements
        if not isinstance(self.__dog, np.ndarray) or self.__dog.ndim != 1:
            raise ValueError(f"Dog position must be a 1D numpy array, got {type(self.__dog)} with shape {self.__dog.shape}")
        #
        
        #creating rendered map view
        if self.__enable_render is True:
            #background
            self.background = pygame.Surface(self.screen.get_size()).convert()
            self.background.fill((255,255,255))
            
            #layer to place forest "maze" on
            self.forest_layer = pygame.SurfaceType(self.screen.get_size()).convert_alpha()
            self.forest_layer.fill((0,0,0,))
            
            #drawing up everything
            self.__draw_map()
            self.__draw_portals()
            self.__draw_dog()
            self.__draw_beginning()
            self.__draw_goal()
            
            #game status updates
    def update(self, mode="human"):
        try:
            img_output = self.__view_update(mode)
            self.__controller_update()
        except Exception as e:
            self.__game_over = True
            self.quit_game()
            raise e
        else: 
            return img_output
                
    #quit functionality
    def quit_game(self):
        try:
            self.__game_over = True
            if self.__enable_render is True:
                pygame.display.quit()
            pygame.quit()
        except Exception:
            pass    
            
    def move_dog(self, dir):
        if dir not in self.__maps.COMPASS.keys():
            raise ValueError(f"{dir} is not a valid direction. Valid directions are {list(self.__maps.COMPASS.keys())}.")
                
        if self.__maps.is_open(self.__dog, dir):
            #update look
            self.__draw_dog(transparency=0)
            #moving dog
            self.__dog += np.array(self.__maps.COMPASS[dir])
            #if dog located on any of the "portal" spots
            if self.maps.is_portal(self.dog):
                self.__dog = np.array(self.maps.get_portal(tuple(self.dog)).teleport(tuple(self.__dog)))
            self.__draw_dog(transparency = 255)
        if not isinstance(self.__dog, np.ndarray) or self.__dog.ndim != 1:
            raise ValueError(f"Dog position must be a 1D numpy array after moving, got {type(self.__dog)} with shape {self.__dog.shape}")
                    
    def reset_dog(self):
        self.__draw_dog(transparency = 0)
        self.__dog = np.zeros(2, dtype=int)
        self.__draw_dog(transparency = 255)
                
    def __controller_update(self):
        if not self.__game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__game_over = True
                    self.quit_game()
                            
    def __view_update(self, mode="human"):
        if not self.__game_over:
            #map and dog location updates
            self.__draw_beginning()
            self.__draw_goal()
            self.__draw_dog()
            self.__draw_portals()
                    
                    
            #updating on screen
            self.screen.blit(self.background, (0,0))
            self.screen.blit(self.forest_layer, (0,0))
                    
            if mode == "human":
                pygame.display.flip()
                    
            #rotate for easier viewing and 3d to 2d surface
            #source: https://www.pygame.org/docs/ref/surfarray.html
            return np.flipud(np.rot90(pygame.surfarray.array3d(pygame.display.get_surface())))

            
    def __draw_map(self):
                
        if self.__enable_render is False:
            return
                
        #line configs
        #color
        line_color = (0,0,0,255)
        #horizontal lines
        for y in range(self.maps.MAP_H + 1):
            pygame.draw.line(self.forest_layer, line_color, (0, y * self.CELL_H),
                                     (self.SCREEN_W, y * self.CELL_H))
        #vertical lines
        for x in range(self.maps.MAP_W + 1):
            pygame.draw.line(self.forest_layer, line_color, (x * self.CELL_W, 0),
                                     (x * self.CELL_W, self.SCREEN_H))
        #walls and wall status
        for x in range(len(self.maps.map_cells)):
            for y in range(len(self.maps.map_cells[x])):
                wall_status = self.maps.get_wall_status(self.maps.map_cells[x,y])
                dirs = ""
                for dir, open in wall_status.items():
                    if open:
                        dirs += dir
                self.__cover_walls(x, y, dirs)
            
    def __cover_walls(self, x, y, dirs, color=(0,0,255,15)):
        if self.__enable_render is False:
            return  
                
        dx = x * self.CELL_W
        dy = y * self.CELL_H
                
        if not isinstance(dirs,str):
            raise TypeError("Directory must be of type str")   
                
        #cardinal directions and line shape
        for dir in dirs:
            if dir == "S":
                line_head = (dx + 1, dy + self.CELL_H)
                line_tail = (dx + self.CELL_W - 1, dy + self.CELL_H)
            elif dir == "N":
                line_head = (dx + 1, dy)
                line_tail = (dx + self.CELL_W - 1, dy)
            elif dir == "W":
                line_head = (dx, dy + 1)
                line_tail = (dx, dy + self.CELL_H - 1)
            elif dir == "E":
                line_head = (dx + self.CELL_W, dy + 1)
                line_tail = (dx + self.CELL_W, dy + self.CELL_H - 1)
            else:
                raise ValueError("Directions must be: (N, S, E, or W).")
                    
            # pygame.draw.lines(self.forest_layer, color, line_head, line_tail)
            pygame.draw.lines(self.forest_layer, color, False, [line_head, line_tail])
            
    def __draw_dog(self, color=(0,0,150), transparency=255):
        if self.__enable_render is False:
            return
        x = int(self.__dog[0] * self.CELL_W + self.CELL_W * 0.5 + 0.5)
        y = int(self.__dog[1] * self.CELL_H + self.CELL_H * 0.5 + 0.5)
        r = int(min(self.CELL_W, self.CELL_H)/5 + 0.5)
                
        pygame.draw.circle(self.forest_layer, color + (transparency,), (x,y), r)
                
    def __draw_beginning(self, color=(0, 0, 150), transparency=235):
        self.__color_cell(self.beginning, color=color, transparency=transparency)

    def __draw_goal(self, color=(150, 0, 0), transparency=235):
        self.__color_cell(self.goal, color=color, transparency=transparency)

    def __draw_portals(self, transparency=160):
        if self.__enable_render is False:
            return 
        color_range = np.linspace(0, 255, len(self.maps.portals), dtype=int)
        color_i = 0
        for portal in self.maps.portals:
            color = ((100 - color_range[color_i])% 255, color_range[color_i], 0)
            color_i += 1
            for location in portal.locations:
                self.__color_cell(location, color=color, transparency=transparency)
                        
    def __color_cell(self, cell, color, transparency):
        if self.__enable_render is False:
            return

        if not (isinstance(cell, (list, tuple, np.ndarray)) and len(cell) == 2):
            raise TypeError("Cell must a be a size 2 tuple, list, or numpy array")

        x = int(cell[0] * self.CELL_W + 0.5 + 1)
        y = int(cell[1] * self.CELL_H + 0.5 + 1)
        w = int(self.CELL_W + 0.5 - 1)
        h = int(self.CELL_H + 0.5 - 1)
        pygame.draw.rect(self.forest_layer, color + (transparency,), (x, y, w, h))
                
                
    #using decorators to access properties using @property
            
    @property
    def maps(self):
        return self.__maps
            
    @property
    def dog(self):
        return self.__dog
            
    @property
    def beginning(self):
        return self.__beginning
            
    @property
    def goal(self):
        return self.__goal
            
    @property
    def game_over(self):
        return self.__game_over
            
    @property
    def SCREEN_SIZE(self):
        return tuple(self.__screen_size)
            
    @property
    def SCREEN_W(self):
        return int(self.SCREEN_SIZE[0])

    @property
    def SCREEN_H(self):
        return int(self.SCREEN_SIZE[1])

    @property
    def CELL_W(self):
        return float(self.SCREEN_W) / float(self.maps.MAP_W)

    @property
    def CELL_H(self):
        return float(self.SCREEN_H) / float(self.maps.MAP_H)

class Maps:
    #cardinal directions
    COMPASS = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0)
    }
    
    def __init__(self, map_cells=None, map_size=(10,10), has_loops=True, num_portals=0):
        #map attributes
        self.map_cells = map_cells
        self.has_loops = has_loops
        self.__portals_dict = dict()
        self.__portals = []
        self.num_portals = num_portals
        
        #2d map environment
        if self.map_cells is not None:
            if isinstance(self.map_cells, (np.ndarray,np.generic)) and len(self.map_cells.shape) == 2:
                self.map_size = tuple(map_cells.shape)
            else:
                raise ValueError("Variable 'map_cells' must be a 2D numpy array.")   
            
        #GENERATE RANDOM IF DOESN'T EXIST - COMMENT OUT FOR NOW AND FIX LATER
        else:
            if not(isinstance(map_size, (list, tuple)) and len(map_size) == 2):
                raise ValueError("Variable 'map_size' must be a tuple: (width, height)")
            self.map_size = map_size
            
            #random map gen function
            self.generate_map()
            
    def save_map(self, file_path):
        if not isinstance(file_path, str):
            raise TypeError("Invalid. File path must be of type str.")
        if not os.path.exists(os.path.dirname(file_path)):
            raise ValueError("Cannot find directory for %s." % file_path)
        else:
            np.save(file_path, self.map_cells, fix_imports=True)      
            
        
    @classmethod
    def load_map(cls, file_path):
        if not isinstance(file_path, str):
            raise TypeError("Invalid. File path must be a string.")
        if not os.path.exists(file_path):
            raise ValueError("Cannot find %s." % file_path)
        else:
            return np.load(file_path, fix_imports=True)
        
    def generate_map(self):
            self.map_cells = np.zeros(self.map_size, dtype=int)
            
            #intializing cell attributes and map structures
            current_cell = (random.randint(0, self.MAP_W - 1), random.randint(0, self.MAP_H-1))
            num_cells_visited = 1
            stack = [current_cell]
            
            #visit all cells for generation
            while stack:
                current_cell = stack.pop()
                x0,y0 = current_cell
                
                #cell "neighbors"
                neighbors = dict()
                for dir_key, dir_val in self.COMPASS.items():
                    x1 = x0 + dir_val[0]
                    y1 = y0 + dir_val[1]
                    
                    if 0 <= x1 < self.MAP_W and 0 <= y1 < self.MAP_H:
                        if self.all_walls_intact(self.map_cells[x1,y1]):
                            neighbors[dir_key] = (x1, y1)
                            
                if neighbors:
                    #just randomly select
                    dir = random.choice(tuple(neighbors.keys()))
                    x1,y1 = neighbors[dir]
                    
                    self.map_cells[x1,y1] = self.__remove_walls(self.map_cells[x1,y1], self.__get_opposite_wall(dir))
                    
                    #push current cell to top of stack
                    stack.append(current_cell)
                    
                    #make "neighbor" cell new current cell
                    stack.append((x1,y1))
                    
                    num_cells_visited += 1
                    
            if self.has_loops:
                self.__remove_random_walls(0.2)
                
            if self.num_portals > 0:
                self.__set_random_portals(num_portal_sets=self.num_portals, set_size = 2)
                
    def __remove_random_walls(self, percent):
        num_cells = int(round(self.MAP_H*self.MAP_W*percent))
        cell_ids = random.sample(range(self.MAP_W*self.MAP_H), num_cells)
        
        #each wall
        for cell_id in cell_ids:
            x = cell_id % self.MAP_H
            y = int(cell_id/self.MAP_H)
            
        #random direction
        dirs = random.sample(list(self.COMPASS.keys()), len(self.COMPASS))
        for dir in dirs:
            #remove wall if not already done
            if self.is_removable((x, y), dir):
                self.map_cells[x, y] = self.__remove_walls(self.map_cells[x, y], dir)
                break
    
    def __set_random_portals(self, num_portal_sets, set_size=2):
        num_portal_sets = int(num_portal_sets)
        set_size = int(set_size)

        #portals cannot exceed size of map
        max_portal_sets = int(self.MAP_W * self.MAP_H / set_size)
        num_portal_sets = min(max_portal_sets, num_portal_sets)

        cell_ids = random.sample(range(1, self.MAP_W * self.MAP_H - 1), num_portal_sets*set_size)

        for i in range(num_portal_sets):
            portal_cell_ids = random.sample(cell_ids, set_size)
            portal_locations = []
            for portal_cell_id in portal_cell_ids:
                cell_ids.pop(cell_ids.index(portal_cell_id))
                #convert portal id to location
                x = portal_cell_id % self.MAP_H
                y = int(portal_cell_id / self.MAP_H)
                portal_locations.append((x,y))
            portal = Portal(*portal_locations)
            self.__portals.append(portal)

            #portal dict
            for portal_location in portal_locations:
                self.__portals_dict[portal_location] = portal
          
    #making sure wall isn't there, and things are in bounds of map      
    def is_open(self, cell_id, dir):
        x1 = cell_id[0] + self.COMPASS[dir][0]
        y1 = cell_id[1] + self.COMPASS[dir][1]
        
        if self.is_within_bounds(x1, y1):
            this_wall = bool(self.get_wall_status(self.map_cells[cell_id[0], cell_id[1]])[dir])
            other_wall = bool(self.get_wall_status(self.map_cells[x1, y1])[self.__get_opposite_wall(dir)])
            return this_wall or other_wall
        return False
    
    #check to see if wall that will be removed during generation is in bounds
    def is_removable(self, cell_id, dir):
        x1 = cell_id[0] + self.COMPASS[dir][0]
        y1 = cell_id[1] + self.COMPASS[dir][1]
        
        return not self.is_open(cell_id, dir) and self.is_within_bounds(x1,y1)
    
    def is_within_bounds(self, x, y):
        return 0 <= x < self.MAP_W and 0 <= y < self.MAP_H
    
    def is_portal(self, cell):
        return tuple(cell) in self.__portals_dict
    
    #portals and map size adjustments with decorators
    @property
    def portals(self):
        return tuple(self.__portals)
    
    def get_portal(self, cell):
        if cell in self.__portals_dict:
            return self.__portals_dict[cell]
        return None
    
    #map width and height
    @property
    def MAP_W(self):
        return int(self.map_size[0])
    
    @property
    def MAP_H(self):
        return int(self.map_size[1])
    
    @classmethod
    def get_wall_status(cls, cell):
        #keys in dictionary are NSEW directions - checking for status of "yes wall - 1" or "no wall - 0"
        #saw recommendation to use this on stackoverflow. 
        #source and reference for "bitwise operation" that I learned: https://realpython.com/python-bitwise-operators/
        walls = {
            "N" : (cell & 0x1) >> 0,
            "E" : (cell & 0x2) >> 1,
            "S" : (cell & 0x4) >> 2,
            "W" : (cell & 0x8) >> 3,
        }
        return walls
    
    #same hexidecimal checking
    @classmethod
    def all_walls_intact(cls, cell):
        return cell & 0xF == 0
    
    @classmethod
    def num_walls_removed(cls, cell):
        walls = cls.get_wall_status(cell)
        num_removed = 0
        for wall_removed in walls.values():
            num_removed += wall_removed 
        return num_removed
    
    @classmethod
    def __remove_walls(cls, cell, dirs):
        if "N" in dirs:
            cell |= 0x1
        if "E" in dirs:
            cell |= 0x2
        if "S" in dirs:
            cell |= 0x4
        if "W" in dirs:
            cell |= 0x8
        return cell 
    
    @classmethod
    def __get_opposite_wall(cls, dirs):

        if not isinstance(dirs, str):
            raise TypeError("Directory must be of type str.")

        opposite_dirs = ""

        for dir in dirs:
            if dir == "N":
                opposite_dir = "S"
            elif dir == "S":
                opposite_dir = "N"
            elif dir == "E":
                opposite_dir = "W"
            elif dir == "W":
                opposite_dir = "E"
            else:
                raise ValueError("Only N, S, E, W are possible directions.")

            opposite_dirs += opposite_dir

        return opposite_dirs

#POSSIBLE REMOVE - LIKELY WILL NOT KEEP PORTALS   
class Portal:
    
    def __init__(self, *locations):

        self.__locations = []
        for location in locations:
            if isinstance(location, (tuple, list)):
                self.__locations.append(tuple(location))
            else:
                raise ValueError("Portal location must be of type tuple or list.")

    def teleport(self, cell):
        if cell in self.locations:
            return self.locations[(self.locations.index(cell) + 1) % len(self.locations)]
        return cell

    def get_index(self, cell):
        return self.locations.index(cell)

    @property
    def locations(self):
        return self.__locations
    
    
if __name__ == "__main__":
    maps = ForestViews(screen_size = (600, 600), map_size=(10,10))
    maps.update()
    input("Press any key to quit game.")