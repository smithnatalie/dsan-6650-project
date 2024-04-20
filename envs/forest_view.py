import pygame
import numpy as np
import os

class ForestViews:
    #starting w 10x10
    def __init__(self, view_name = "ForestView", map_file_path=None,
                 map_size=(10, 10), screen_size=(600,600),
                 has_loops=False, num_portals=0, enable_render=True):
        
        #pygame configs
        pygame.init()
        pygame.display.set_caption(view_name)
        self.clock = pygame.time.Clock()
        self.__game_over = False
        self.__enable_render = enable_render
        
        #loading the forest map view
        if map_file_path is None:
            self.__view = Map(map_size=map_size, has_loops=has_loops, num_portals=num_portals)
        else:
            if not os.path.exists(map_file_path):
                dir_path = os.path.dirname(os.path.abspath(__file__))
                rel_path = os.path.join(dir_path, "forest_maps", map_file_path)
                #for error capturing if file not found:
                if os.path.exists(rel_path):
                    map_file_path = rel_path
                else:
                    raise FileExistsError("Unable to locate map %s." % map_file_path)
            self.__view = Map(map_cells=Map.load_map(map_file_path))
            
        self.map_size = self.__view.map_size
        if self.__enable_render is True:
            #showing bottom right area
            self.screen = pygame.display.set_mode(screen_size)
            self.__screen_size = tuple(map(sum, zip(screen_size, (-1, -1))))
            
        #starting point - can change
        self.__beginning = np.zeros(2, dtype=int)
        
        #end goal- rescue spot - can change
        self.__goal = np.array(self.map_size) - np.array(1,1)
        
        #creating agent dog
        self.__dog = self.beginning
        
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
                if dir not in self.__map.COMPASS.keys():
                    raise ValueError("%s is not a valid directory. The only valid directories are %s."
                                     % (str(dir), str(self.__maze.COMPASS.keys())))
                
                if self.__map.is_open(self.__dog, dir):
                    #update look
                    self.__draw_dog(transarency=0)
                    #move dog around
                    self.__dog += np.array(self.__maze.COMPASS[dir])
                    #if dog located on any of the "portal" spots
                    if self.map.is_portal(self.dog):
                        self.__dog = np.array(self.map.get_portal(tuple(self.dog)).teleport(tuple(self.robot)))
                    self.__draw_dog(transparency = 255)
                    
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
                    
                    if mode == "human"
                        pygame.display.flip()
                    
                    #rotate for easier viewing and 3d to 2d surface
                    #source: https://www.pygame.org/docs/ref/surfarray.html
                    return np.flipup(np.rot90(pygame.surfarray.array3d(pygame.display.get_surface())))

            
            def __draw_map(self):
                
                if self.__enable_render is False:
                    return
                
                #line configs
                #color
                line_color = (0,0,0,255)
                #horizontal lines
                for y in range(self.map.MAP_H + 1):
                    pygame.draw.line(self.forest_layer, line_color, (0, y * self.CELL_H),
                                     (self.SCREEN_W, y * self.CELL_H))
                #vertical lines
                for x in range(self.map.MAP_W + 1):
                    pygame.draw.line(self.forest_layer, line_color, (x * self.CELL_W, 0),
                                     (x * self.CELL_W, self.SCREEN_H))
            #walls and wall status
                for x in range(len(self.map.map_cells)):
                    for y in range(len(self.map.map_cells[x])):
                        wall_status = self.map.get_wall_status(self.map.map_cells[x,y])
                        dirs = ""
                        for dir, open in wall_status.items():
                            if open:
                                dirs += dir
                        self.__cover_walls(x, y, dirs)
            
            def __cover_walls(self, x, y, dirs, color=(0,0,255,15)):
                if self.__enable_render is False
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
                    
                    pygame.draw.lines(self.forest_layer, color, line_head, line_tail)
            
                