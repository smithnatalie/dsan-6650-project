import os
import numpy as np
import gymnasium
from gymnasium import spaces
from search_rescue_game.envs.forest_view import ForestViews
from typing import List, Tuple, Dict


######TESTING###############################################

#location of premade maps

MAPS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "map_options")



class MapEnv(gymnasium.Env):
    metadata = {"render.modes": ["human", "rgb_array"]}
    
    actions: List[str] = ["N", "S", "W", "E"]
    
    
    def __init__(self, screen_size: Tuple[int, int] = (600, 600),
                 map_file_path: str = None, map_size: Tuple[int, int]= (10, 10)):
        
        self.map_size: Tuple[int, int] = map_size
        
        #map view for env
        self.map_view: ForestViews = ForestViews(custom_map="Search and Rescue - Map (%d x %d)" % map_size,
                                                 screen_size = screen_size, map_size=map_size,
                                                 map_file_path = map_file_path)
        
        
        #action space
        self.action_space: spaces.Discrete(2 * len(self.map_size))
        
        #obsv space 
        low: np.ndarray = np.zeros(len(self.map_size), dtype=int)
        high: np.ndarray = np.array(self.map_size, dtype=int) - np.ones(len(self.map_size), dtype=int)
        self.observation_space: spaces.Box = spaces.Box(low, high, dtype=np.int64)
    
    #Was having a lot of issues with my previous step function
    # suggestion to generalize from a couple sources:
    # https://stackoverflow.com/questions/10016352/convert-numpy-array-to-tuple
    # https://stackoverflow.com/questions/45957968/float-arguments-and-dict-values-with-numpy
    #Function accepts an action and returns a tuple: observation, reward, terminated, truncated, info
    
    def step(self, action: int or str) -> Tuple[np.array, float, bool, bool, Dict]:
        if isinstance(action, int):
            self.map_view.move_dog(self.actions[action])
        elif isinstance(action, str):
            self.map_view.move_dog(action)
        else:
            raise TypeError("Only 'int' and 'str' are accepted for action types.")
        
        #reward coding - may change this up to add complexity
        #New gymnasium documentation requires "truncated" and "terminated" instead of "done"
        
        if np.array(self.map_view.dog, self.map_view.goal):
            #if the goal/highest reward is reached, terminate game
            reward: float = 1
            terminated: bool = True
            truncated: bool = False
        else:
            #if the goal/highest reward is not reached, do not terminate game and continue
            reward: float = -0.1 / (self.map_size[0] * self.map_size[1])
            terminated: bool = False
            truncated: bool = False
            
        info: Dict = {}    
        
        #5 values we will need in the q-learning game step
        return self.map_view.dog, reward, terminated, truncated, info
    
    #resetting state of the environment so we can run iterations of the game
    def reset(self) -> np.array:
        self.map_view.reset_game()
        return self.map_view.dog
    
    #renders environment
    def render(self, mode: str = 'human'):
        #for my user input
        self.map_view.process_input()
        
        if mode in ['human', 'rgb_array']:
            return self.map_view.render(mode)
        else:
            super(MapEnv, self).render(mode=mode)
            
#10 x 10 Maps
           
class MapEnv10x10(MapEnv):

    def __init__(self):
        super(MapEnv10x10, self).__init__(screen_size=(600, 600), maze_size=(10, 10),
                                                 map_file_path=os.path.join(MAPS_DIR, "mapenv_10x10.npy"))


class RandomMapEnv10x10(MapEnv):

    def __init__(self):
        super(RandomMapEnv10x10, self).__init__(screen_size=(600, 600), maze_size=(10, 10),
                                                 map_file_path=None)

#25 x 25 Maps

class MapEnv25x25(MapEnv):

    def __init__(self):
        super(MapEnv25x25, self).__init__(screen_size=(600, 600), maze_size=(25, 25),
                                                 map_file_path=os.path.join(MAPS_DIR, "mapenv_25x25.npy"))


class RandomMapEnv25x25(MapEnv):

    def __init__(self):
        super(RandomMapEnv25x25, self).__init__(screen_size=(600, 600), maze_size=(25, 25),
                                                 map_file_path=None)

    

##############################################################


# class MapEnv(gymnasium.Env):
#     def __init__(self, map_file=None, map_size=None, mode=None, enable_render=True, render_mode=None, custom_map=False):
#         super(MapEnv, self).__init__()
#         self.enable_render = enable_render
#         self.render_mode = render_mode
        
#         # Decide on map initialization method
#         if map_file:
#             # Initialize from a specific map file
#             self.map_view = ForestViews(map_name=f"Search and Rescue - Map ({map_file})",
#                                         map_file_path=map_file,
#                                         screen_size=(700, 700),
#                                         enable_render=(render_mode == 'rgb_array'))
#         elif custom_map:
#             # Initialize with a custom designed map
#             self.map_view = ForestViews(map_size=map_size or (10, 10),
#                                         screen_size=(700, 700),
#                                         custom_map=True,  # Ensure the ForestViews class supports this
#                                         enable_render=(render_mode == 'rgb_array'))
#         elif map_size:
#             # Initialize with random map generation parameters
#             has_loops = (mode == "plus")
#             num_portals = int(round(min(map_size) / 3)) if mode == "plus" else 0
#             self.map_view = ForestViews(map_name=f"Search and Rescue - Map ({map_size[0]} x {map_size[1]})",
#                                         map_size=map_size,
#                                         has_loops=has_loops,
#                                         num_portals=num_portals,
#                                         screen_size=(700, 700),
#                                         enable_render=(render_mode == 'rgb_array'))
#         else:
#             raise ValueError("A valid map_file, map_size, or custom_map must be provided")

#         self.action_space = spaces.Discrete(4)  # Assuming 4 directions
#         low = np.zeros(len(self.map_size), dtype=int)
#         high = np.array(self.map_size, dtype=int) - 1
#         self.observation_space = spaces.Box(low, high, dtype=np.int64)
#         self.reset()


# class MapEnv(gymnasium.Env):
#     metadata = {"render_modes": ["human", "rgb_array"],
#                 #used ChatGPT to help me by implementing render_fps after logger warnings
#                 "render_fps" : 30,
#                 }

#     ACTION = ["N", "S", "E", "W"]

#     def __init__(self, map_file=None, map_size=None, mode=None, enable_render=True, render_mode=None):
#         super(MapEnv, self).__init__()
#         self.viewer = None
#         self.enable_render = enable_render
#         self.render_mode = render_mode
#         # self.seed = None

#         if map_file:
#             self.map_view = ForestViews(map_name=f"Search and Rescue - Map ({map_file})",
#                                         map_file_path=map_file,
#                                         screen_size=(700, 700),
#                                         enable_render=(render_mode == 'rgb_array'),
#                                         ) 
#                                         # enable_render=enable_render)
#             self.map_size = self.map_view.map_size
#         elif map_size:
#             has_loops = (mode == "plus")
#             num_portals = int(round(min(map_size) / 3)) if mode == "plus" else 0
#             self.map_view = ForestViews(
#                 map_name=f"Search and Rescue - Map ({map_size[0]} x {map_size[1]})",
#                 map_size=map_size,
#                 screen_size=(700, 700),
#                 has_loops=has_loops,
#                 num_portals=num_portals,
#                 enable_render=(render_mode == 'rgb_array'),
#             )
#             self.map_size = map_size
#         else:
#             raise ValueError("A valid map_file or map_size must be provided")


#         if self.seed is not None:
#             self.seed()


#         #actions - forwards and backwards in each direction possible
#         # self.action_space = spaces.Discrete(2*len(self.map_size))
#         self.action_space = spaces.Discrete(4)  # Assuming 4 directions
#         #observation spaces
#         low = np.zeros(len(self.map_size), dtype=int)
#         high = np.array(self.map_size, dtype=int) - 1
#         self.observation_space = spaces.Box(low, high, dtype=np.int64)

#         #initial state
#         self.state = None
#         # self.steps_beyond_done = None

#         #other intializations needed to play
#         # self.seed()
#         self.reset()
        # self.configure()
        
        
    # def __del__(self):
    #     if hasattr(self, 'enable_render') and self.enable_render:
    #         self.map_view.quit_game()
    # # def __del__(self):
    # #     if self.enable_render is True:
    # #         self.map_view.quit_game()

    # def configure(self, display=None):
    #     self.display = display

    #REWARDS and steps
    #source for assistance with termination + truncation stuff (most resources had old gym documentation)
    # https://stackoverflow.com/questions/77042526/how-to-record-and-save-video-of-gym-environment
    
    # def step(self, action):
    #     self.map_view.move_dog(self.ACTION[action])

    #     if np.array_equal(self.map_view.dog, self.map_view.goal):
    #         reward = 1
    #         # done = True
    #         terminated = True
    #         truncated = False
    #     else:
    #         reward = -0.1 / (self.map_size[0] * self.map_size[1])
    #         # done = False
    #         terminated = True
    #         truncated = False

    #     self.state = np.array(self.map_view.dog, dtype=np.int64)
        
    #     #debugging statements
    #     # print("State after action:", self.state)
    #     # print("Type of state:", type(self.state))
    #     # print("Shape of state:", self.state.shape)
        
    #     info = {}
    #     return self.state, reward, terminated, truncated, info

    # def seed(self, seed_value=None):
    #     self.np_random, seed_value = seeding.np_random(seed_value)
    #     return [seed_value]

    # def step(self, action):
    #     if isinstance(action, int):
    #         self.map_view.move_dog(self.ACTION[action])
    #     else:
    #         self.map_view.move_dog(action)
            
    #     #debugging statements
        
    #     print("Dog position:", self.map_view.dog)
    #     print("Type of dog position:", type(self.map_view.dog))
    #     #

    #     if np.array_equal(self.map_view.dog, self.map_view.goal):
    #         reward = 1
    #         done = True
    #     else:
    #         reward = -0.1/(self.map_size[0]*self.map_size[1])
    #         done = False

    #     self.state = self.map_view.dog
        
    #     #debugging statements
    #     print("State after move:", self.state)
    #     print("Type of state:", type(self.state))
    #     #
        
    #     info = {}

    #     return self.state, reward, done, info
    

    #def reset(self, seed=None, options=None):
    # def reset(self, **kwargs):#seed = None):
    #     seed = kwargs.get('seed', None)
    #     self.np_random, seed = seeding.np_random(seed)
    #     #want 1D array
    #     self.state = np.array([0,0], dtype=int)#np.zeros(2, dtype=np.int64)
    #     self.map_view.reset_dog()
    #     self.steps_beyond_done = None
    #     self.done = False
    #     return self.state, {}
    

    # def is_game_over(self):
    #     return self.map_view.game_over

    # def render(self, mode="human", close=False):
    #     if close:
    #         self.map_view.quit_game()

    #     return self.map_view.update(mode)
    
#map classes
    
# class ForestMap10x10(MapEnv):
#     def __init__(self, render_mode='rgb_array'):
#     # def __init__(self, enable_render=True):
        
#         super(ForestMap10x10, self).__init__(map_file="forestmap_10x10.npy", enable_render=enable_render)

# class RandomForestMap10x10(MapEnv):
#     def __init__(self, render_mode='rgb_array'):
#     # def __init__(self, enable_render=True):
#         super(RandomForestMap10x10, self).__init__(map_size=(10, 10), enable_render=enable_render)

#THIS IS THE ONE I AM USING


# class RandomForestMap10x10Plus(MapEnv):
#     def __init__(self, enable_render=True, render_mode='rgb_array'):
#         super(RandomForestMap10x10Plus, self).__init__(map_size=(10, 10), mode="plus", enable_render=enable_render, render_mode=render_mode, custom_map=True)


# class CustomForestMap10x10(MapEnv):
#     def __init__(self, enable_render=True, render_mode='rgb_array', custom_map = False):
#         super(CustomForestMap10x10, self).__init__(map_size=(10, 10), mode="plus", enable_render=enable_render, render_mode=render_mode, custom_map=True)


# class ForestMap10x10(MapEnv):
#     def __init__(self, enable_render = True, render_mode='rgb_array'):
#         super(ForestMap10x10, self).__init__(map_file="map_003.npy", enable_render=enable_render, render_mode=render_mode)
