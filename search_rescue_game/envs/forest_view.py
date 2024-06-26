import numpy as np
import pygame
from typing import Tuple
from .forest_map import Maps, Cell
from pygame.locals import *


#TESTING~>~>~>~>~>~>~>>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~

class ForestViews:
    #colors for map - this is where customization will go once things are workign
    
    BACKGROUND_COLOR = (255, 255, 255, 255)
    GAME_SURFACE_COLOR = (0, 0, 0, 0)
    LINE_COLOR = (0, 0, 0, 255)
    WALL_COLOR = (0, 0, 255, 15)

    def __init__(self, caption: str = "Search and Rescue!", screen_size: Tuple[int,int] = (600,600),
                 map_size: tuple[int,int] = (10,10), map_file_path = None):
        
        #intializing the game
        pygame.init()
        pygame.display.set_caption(caption)
        
        #screen and map sizes
        self.__screen_width: int = screen_size[0]
        self.__screen_height: int = screen_size[1]
        self.__screen: pygame.Surface = pygame.display.set_mode((self.__screen_width + 1, self.__screen_height + 1))
        self.__map_size: Tuple[int, int] = map_size

        #individual cells/spaces that make up map- just going to do floor div so no remainder, all same size
        self.__cell_height: int = self.__screen_height // map_size[1]
        self.__cell_width: int = self.__screen_width // map_size[0]
    
        #starting spot and goal for dog - may change location of these 
        self.__beginning: np.ndarray = np.zeros(2, dtype=int)
        self.__goal: np.ndarray = np.array(map_size) - np.array((1,1))
        self.__dog: np.ndarray = np.zeros(2, dtype=int)
        
        #background and game surfaces
        self.__background: pygame.Surface = pygame.Surface(self.__screen.get_size()).convert()
        self.__background.fill(self.BACKGROUND_COLOR)
        
        self.__game_surface: pygame.Surface = pygame.Surface(self.__screen.get_size()).convert_alpha(self.__screen)
        self.__game_surface.fill(self.GAME_SURFACE_COLOR)
        
        #if want to create new map 
        self.__map: Maps = Maps(map_size=map_size, map_file_path=map_file_path)
    

        #dog icon
        self.__dog_icon = pygame.image.load('./search_rescue_game/envs/images/bloodhound.png')
            #scale to fit cell
        self.__dog_icon = pygame.transform.scale(self.__dog_icon, (self.__cell_width, self.__cell_height))
        
        #goal (baby) icon
        self.__goal_icon = pygame.image.load('./search_rescue_game/envs/images/baby.png')
        self.__goal_icon = pygame.transform.scale(self.__goal_icon, (self.__cell_width, self.__cell_height))
        
        
        #cover - fog of war forest icon
        self.__cover_icon = pygame.image.load('./search_rescue_game/envs/images/tree.png')
        self.__cover_icon = pygame.transform.scale(self.__cover_icon, (self.__cell_width, self.__cell_height))
        
        #dirt path icon
        self.__beginning_icon = pygame.image.load('./search_rescue_game/envs/images/dirt.png')
        self.__beginning_icon = pygame.transform.scale(self.__beginning_icon, (self.cell_width, self.cell_height))

        self.__path_icon = pygame.image.load('./search_rescue_game/envs/images/dirt.png')
        self.__path_icon = pygame.transform.scale(self.__path_icon, (self.cell_width, self.cell_height))
        
        
        
        #####
        
        #initializing "fog" state
        self.__coverage = np.full((self.map_width, self.map_height), True)
        
        #leave beginning cell uncovered
        self.__coverage[self.beginning[0], self.beginning[1]] = False
        
        #drawing the objects so they show up - will define below
        self.__draw_map()
        self.__beginning_color()
        self.__goal_color() ###THIS WILL LIKELY CHANGE TO AN ICON
        self.__dog_color() ###THIS WILL LIKELY CHANGE TO AN ICON
    
    
    def __draw_map(self):
        #horizontal lines
        for x in range(self.map_width + 1):
            pygame.draw.line(self.__game_surface,
                             self.LINE_COLOR,
                             (x * self.cell_width, 0),
                             (x * self.cell_width, self.screen_height))
        
        #vertical lines
        for y in range(self.map_height + 1):
            pygame.draw.line(self.__game_surface,
                             self.LINE_COLOR,
                             (0, y * self.__cell_height),
                             (self.screen_width, y * self.cell_height))
      
        #draw and break up "maze" style walls - may possibly change to icons too - trees
        for x in range(self.map_width):
            for y in range(self.map_height):
                for direction in ["N", "S", "E", "W"]:
                    if not self.__map.cells[x][y].walls[direction]:
                        self.__color_wall(x, y, direction, self.WALL_COLOR)   
                        
    
    def __color_wall(self, x: int, y: int, direction: str, color: Tuple[int, int, int, int] = (0, 0, 255, 15)): 
        dx: int = x * self.cell_width
        dy: int = y * self.cell_height
        
        #color walls based on north, south, west, east directions
        if direction == 'N':
            pygame.draw.line(self.__game_surface, color,
                             (dx + 1, dy),
                             (dx + self.cell_width - 1, dy))
        elif direction == 'S':
            pygame.draw.line(self.__game_surface, color,
                             (dx + 1, dy + self.cell_width),
                             (dx + self.cell_width - 1, dy + self.cell_height))
        elif direction == 'W':
            pygame.draw.line(self.__game_surface, color,
                             (dx, dy + 1),
                             (dx, dy + self.cell_height - 1))
        elif direction == 'E':
            pygame.draw.line(self.__game_surface, color,
                             (dx + self.cell_width, dy + 1),
                             (dx + self.cell_width, dy + self.cell_height - 1))
        else:
            raise ValueError("Only directions of N, S, W and E are accepted.")    
        
    
    def __color_cell(self, x: int, y: int, color: Tuple[int, int, int, int] = (255, 0, 0, 255)):
        x0: int = x * self.cell_width + 1
        y0: int = y * self.cell_height + 1
        w0: int = self.cell_width - 1
        h0: int = self.cell_height - 1
        
        #drawing rectangular shaped spaces: https://www.pygame.org/docs/ref/draw.html#pygame.draw.rect
        pygame.draw.rect(self.__game_surface, color, (x0, y0, w0, h0))
        
    #may change color in accordance with game design     
    def __beginning_color(self, color: Tuple[int, int, int, int] = (0, 0, 0, 0)):
        self.__color_cell(self.beginning[0], self.beginning[1], color)
        
    
    #will likely change to icon to signify area for rescue
    # def __goal_color(self, color: Tuple[int, int, int, int] = (255, 0, 0, 150)):
    #     self.__color_cell(self.goal[0], self.goal[1], color)
    
    def __goal_color(self):
        x0 = self.goal[0] * self.cell_width + (self.cell_width - self.__goal_icon.get_width()) // 2
        y0 = self.goal[1] * self.cell_height + (self.cell_height - self.__goal_icon.get_height()) // 2

        self.__game_surface.blit(self.__goal_icon, (x0, y0))
    
    
    #will change to dog icon - currently just colored circle for testing purposes
    def __dog_color(self):
        #top left to center icon
        x0 = self.dog[0] * self.cell_width + (self.cell_width - self.__dog_icon.get_width()) // 2
        y0 = self.dog[1] * self.cell_height + (self.cell_height - self.__dog_icon.get_height()) // 2

        self.__game_surface.blit(self.__dog_icon, (x0, y0))

    
# decorators, processes, rendering

    @staticmethod
    def process_input():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

    #flipping array with np.flipud - this seems pretty standard across a lot of pygame renders     
    def render(self, mode="human") -> np.flipud:
        self.__screen.blit(self.__background, (0,0))
        self.__screen.blit(self.__game_surface, (0,0))

        #drawing all of the game element we just defined
        self.__draw_map()
        self.__beginning_color()
        self.__dog_color()
        
        
        #cover icons fog
        for x in range(self.map_width):
            for y in range(self.map_height):
                self.__redraw_cell(x,y)
                # if self.__coverage[x,y]:
                #     dx = x * self.cell_width
                #     dy = y * self.cell_height
                #     self.__screen.blit(self.__cover_icon, (dx,dy))
        
        
        
        self.__goal_color()
        
        self.__screen.blit(self.__game_surface, (0,0))
        
        if mode == "human":
            pygame.display.flip()
        
        #source: https://www.pygame.org/docs/tut/SurfarrayIntro.html
        return np.flipud(np.rot90(pygame.surfarray.array3d(pygame.display.get_surface())))


    #movement of our dog agent
    def move_dog(self, direction: str):
        current_cell: Cell = self.__map.cells[self.dog[0]][self.dog[1]]
        
        if not current_cell.walls[direction]:
            old_x, old_y = self.__dog[0], self.__dog[1]

            self.__dog += Maps.compass[direction]
            
            self.__redraw_cell(old_x, old_y)

            self.__coverage[self.__dog[0], self.__dog[1]] = False
            
            self.__redraw_cell(self.__dog[0], self.__dog[1])
        
        

        # if not current_cell.walls[direction]:
        #     #self.__dog_color(transparency=0)
        #     #fixing dog icon trail - want to disappear once moved
        #     x0 = self.dog[0] * self.cell_width
        #     y0 = self.dog[1] * self.cell_height
        #     self.__game_surface.fill(self.BACKGROUND_COLOR, (x0, y0, self.cell_width, self.cell_height))
            
        #     #move
        #     self.__dog = self.dog + Maps.compass[direction]

        #     #uncover cell when dog moves
            
        #     self.__coverage[self.dog[0], self.dog[1]] = False


        self.__dog_color()
        
    
    #this is how dog willl be placed back at starting space and game restarted
    
    #testing reset game w reinstantiation of full coverage tree map
    def reset_game(self):
        self.__dog = np.copy(self.__beginning)
        #reset "fog"
        self.__coverage = np.full((self.map_width, self.map_height), True)
        #reveal starting position on map
        self.__coverage[self.__beginning[0], self.__beginning[1]] = False
        
        self.__game_surface.fill(self.BACKGROUND_COLOR)
        
        self.__draw_map()
        self.__beginning_color
        self.__goal_color()
        self.__dog_color()
        
        for x in range(self.map_width):
            for y in range(self.map_height):
                if self.__coverage[x, y]:
                    dx = x * self.cell_width
                    dy = y * self.cell_height
                    self.__game_surface.blit(self.__cover_icon, (dx, dy))
        
        self.render()
        
        
        
    def __redraw_cell(self, x:int, y:int):
        top_left_x = x * self.cell_width
        top_left_y = y * self.cell_height
        
        if not self.__coverage[x,y]:
            self.__game_surface.blit(self.__path_icon, (top_left_x, top_left_y))
        else:
            self.__game_surface.blit(self.__cover_icon, (top_left_x, top_left_y))
            
            
        if (x, y) == (self.__beginning[0], self.__beginning[1]):
            self.__game_surface.blit(self.__beginning_icon, (top_left_x, top_left_y))
        elif (x, y) == (self.__goal[0], self.__goal[1]):
            self.__game_surface.blit(self.__goal_icon, (top_left_x, top_left_y))
            
        #draw dog if in cell
        if (x,y) == (self.__dog[0], self.__dog[1]):
            self.__dog_color()
    
    
    #decorators 
    @property
    def screen_width(self) -> int:
        return self.__screen_width

    @property
    def screen_height(self) -> int:
        return self.__screen_height

    @property
    def map_width(self) -> int:
        return self.__map_size[0]

    @property
    def map_height(self) -> int:
        return self.__map_size[1]

    @property
    def cell_width(self) -> int:
        return self.__cell_width

    @property
    def cell_height(self) -> int:
        return self.__cell_height

    @property
    def beginning(self) -> np.array:
        return self.__beginning

    @property
    def goal(self) -> np.array:
        return self.__goal

    @property
    def dog(self) -> np.array:
        return self.__dog
    
    
#~>~>~>~>~>>~>~>~>~~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>    