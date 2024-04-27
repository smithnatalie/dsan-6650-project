import os
import numpy as np
import gymnasium
from gymnasium import spaces
from .forest_view import ForestViews
from typing import List, Tuple, Dict
import random


######TESTING###############################################

#location of premade maps

MAPS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "map_options")



class MapEnv(gymnasium.Env):
    metadata = {"render_modes": ["human", "rgb_array"]}
    
    actions: List[str] = ["N", "S", "W", "E"]
    
    def __init__(self, screen_size=(600, 600), map_size=(10, 10), map_file_path=None, render_mode=None):
        super().__init__()
        self.render_mode = render_mode
        
        self.map_size: Tuple[int, int] = map_size
        
        #map view for env
        self.map_view: ForestViews = ForestViews(caption="Search and Rescue - Map (%d x %d)" % map_size,
                                                 screen_size = screen_size, map_size=map_size,
                                                 map_file_path = map_file_path)
        
        
        
        #action space
        self.action_space: spaces = spaces.Discrete(2 * len(self.map_size))
    
        
        #obsv space 
        low: np.ndarray = np.zeros(len(self.map_size), dtype=int)
        high: np.ndarray = np.array(self.map_size, dtype=int) - np.ones(len(self.map_size), dtype=int)
        self.observation_space: spaces.Box = spaces.Box(low, high, dtype=np.int64)
    
    
    def seed(self, seed=None):
        np.random.seed(seed)
        random.seed(seed)
        return [seed]

    #Was having a lot of issues with my previous step function
    # suggestion to generalize from a couple sources:
    # https://stackoverflow.com/questions/10016352/convert-numpy-array-to-tuple
    # https://stackoverflow.com/questions/45957968/float-arguments-and-dict-values-with-numpy
    #Function accepts an action and returns a tuple: observation, reward, terminated, truncated, info
    
    # def step(self, action: int or str) -> Tuple[np.array, float, bool, bool, Dict]:
    #debugging intialization here
    def step(self, action) -> Tuple[np.array, float, bool, bool, Dict]:
        if not (isinstance(action, int) and 0 <= action < self.action_space.n):
            raise ValueError("Action must be an integer within range of defined actions.")
        
        if isinstance(action, int):
            self.map_view.move_dog(self.actions[action])
        elif isinstance(action, str):
            self.map_view.move_dog(action)
        else:
            raise TypeError("Only 'int' and 'str' are accepted for action types.")
        
        #reward coding - may change this up to add complexity
        #New gymnasium documentation requires "truncated" and "terminated" instead of "done"
        
        if np.array_equal(self.map_view.dog, self.map_view.goal):
            # Code when dog reaches the goal
            reward = 1
            terminated = True
            truncated = False
        else:
            # Code for ongoing game
            reward = -0.1 / (self.map_size[0] * self.map_size[1])
            terminated = False
            truncated = False
            
        info: Dict = {}    
        
        #5 values we will need in the q-learning game step
        return self.map_view.dog, reward, terminated, truncated, info
    
    
    #debugging
    def reset(self, seed=None, options=None) -> Tuple[np.array, Dict]:
        if seed is not None:
            np.random.seed(seed)
            
        #reset
        self.map_view.reset_game()
        
        return self.map_view.dog, {}
    
    #renders environment
    def render(self):
        if self.render_mode == "human":
            self.map_view.process_input()
            return self.map_view.render(self.render_mode)
        elif self.render_mode == "rgb_array":
            return self.map_view.render(self.render_mode)
        else:
            super(MapEnv, self).render()
            
#10 x 10 Maps
           
class MapEnv10x10(MapEnv):

    def __init__(self):
        super(MapEnv10x10, self).__init__(screen_size=(600, 600), map_size=(10, 10),
                                                 map_file_path=os.path.join(MAPS_DIR, "mapenv_10x10.npy"))


# class RandomMapEnv10x10(MapEnv):

#     def __init__(self):
#         super(RandomMapEnv10x10, self).__init__(screen_size=(600, 600), map_size=(10, 10),
#                                                  map_file_path=None)

#test to debug gymnasium documentation quirks 

#current one being used:

class RandomMapEnv10x10(MapEnv):
    def __init__(self, screen_size=(600,600), map_size=(10,10), map_file_path=None, render_mode=None):
        super().__init__(screen_size=screen_size, map_size=map_size, map_file_path=map_file_path, render_mode=render_mode)

#25 x 25 Maps

class MapEnv25x25(MapEnv):

    def __init__(self):
        super(MapEnv25x25, self).__init__(screen_size=(600, 600), map_size=(25, 25),
                                                 map_file_path=os.path.join(MAPS_DIR, "mapenv_25x25.npy"))


class RandomMapEnv25x25(MapEnv):

    def __init__(self):
        super(RandomMapEnv25x25, self).__init__(screen_size=(600, 600), map_size=(25, 25),
                                                 map_file_path=None)


