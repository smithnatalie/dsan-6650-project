import numpy as np

import gymnasium
from gymnasium import error, spaces, utils
from gymnasium.utils import seeding
from .forest_view import ForestViews


class MapEnv(gymnasium.Env):
    metadata = {"render_modes": ["human", "rgb_array"],
                #used ChatGPT to help me by implementing render_fps after logger warnings
                "render_fps" : 30,
                }

    ACTION = ["N", "S", "E", "W"]

    def __init__(self, map_file=None, map_size=None, mode=None, enable_render=True, render_mode=None):
        super(MapEnv, self).__init__()
        self.viewer = None
        self.enable_render = enable_render
        self.render_mode = render_mode
        # self.seed = None

        if map_file:
            self.map_view = ForestViews(map_name=f"Search and Rescue - Map ({map_file})",
                                        map_file_path=map_file,
                                        screen_size=(700, 700),
                                        enable_render=(render_mode == 'rgb_array'),
                                        ) 
                                        # enable_render=enable_render)
            self.map_size = self.map_view.map_size
        elif map_size:
            has_loops = (mode == "plus")
            num_portals = int(round(min(map_size) / 3)) if mode == "plus" else 0
            self.map_view = ForestViews(
                map_name=f"Search and Rescue - Map ({map_size[0]} x {map_size[1]})",
                map_size=map_size,
                screen_size=(700, 700),
                has_loops=has_loops,
                num_portals=num_portals,
                enable_render=(render_mode == 'rgb_array'),
            )
            self.map_size = map_size
        else:
            raise ValueError("A valid map_file or map_size must be provided")


        if self.seed is not None:
            self.seed()


        #actions - forwards and backwards in each direction possible
        # self.action_space = spaces.Discrete(2*len(self.map_size))
        self.action_space = spaces.Discrete(4)  # Assuming 4 directions
        #observation spaces
        low = np.zeros(len(self.map_size), dtype=int)
        high = np.array(self.map_size, dtype=int) - 1
        self.observation_space = spaces.Box(low, high, dtype=np.int64)

        #initial state
        self.state = None
        # self.steps_beyond_done = None

        #other intializations needed to play
        # self.seed()
        self.reset()
        # self.configure()
        
        
    def __del__(self):
        if hasattr(self, 'enable_render') and self.enable_render:
            self.map_view.quit_game()
    # def __del__(self):
    #     if self.enable_render is True:
    #         self.map_view.quit_game()

    def configure(self, display=None):
        self.display = display

    #REWARDS and steps
    #source for assistance with termination + truncation stuff (most resources had old gym documentation)
    # https://stackoverflow.com/questions/77042526/how-to-record-and-save-video-of-gym-environment
    
    def step(self, action):
        self.map_view.move_dog(self.ACTION[action])

        if np.array_equal(self.map_view.dog, self.map_view.goal):
            reward = 1
            # done = True
            terminated = True
            truncated = False
        else:
            reward = -0.1 / (self.map_size[0] * self.map_size[1])
            # done = False
            terminated = True
            truncated = False

        self.state = np.array(self.map_view.dog, dtype=np.int64)
        
        #debugging statements
        # print("State after action:", self.state)
        # print("Type of state:", type(self.state))
        # print("Shape of state:", self.state.shape)
        
        info = {}
        return self.state, reward, terminated, truncated, info

    def seed(self, seed_value=None):
        self.np_random, seed_value = seeding.np_random(seed_value)
        return [seed_value]

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
    def reset(self, **kwargs):#seed = None):
        seed = kwargs.get('seed', None)
        self.np_random, seed = seeding.np_random(seed)
        #want 1D array
        self.state = np.array([0,0], dtype=int)#np.zeros(2, dtype=np.int64)
        self.map_view.reset_dog()
        self.steps_beyond_done = None
        self.done = False
        return self.state, {}
    

    def is_game_over(self):
        return self.map_view.game_over

    def render(self, mode="human", close=False):
        if close:
            self.map_view.quit_game()

        return self.map_view.update(mode)
    
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

class RandomForestMap10x10Plus(MapEnv):
    def __init__(self, enable_render=True, render_mode='rgb_array'):
        super(RandomForestMap10x10Plus, self).__init__(map_size=(10, 10), mode="plus", enable_render=enable_render, render_mode=render_mode)




# class RandomForestMap10x10Plus(MapEnv):
#     def __init__(self, enable_render = True, render_mode='rgb_array'):
#         super(RandomForestMap10x10Plus, self).__init__(map_size=(10, 10), mode="plus", enable_render=enable_render, render_mode=render_mode)
    
    
    
    
    
    
     # super().__init__(map_size=(10, 10), mode="plus", enable_render=True, render_mode=render_mode)
# map configurations - GO THRU AND REMOVE LATER!
# class MazeEnvSample5x5(MazeEnv):

#     def __init__(self, enable_render=True):
#         super(MazeEnvSample5x5, self).__init__(maze_file="maze2d_5x5.npy", enable_render=enable_render)


# class MazeEnvRandom5x5(MazeEnv):

#     def __init__(self, enable_render=True):
#         super(MazeEnvRandom5x5, self).__init__(maze_size=(5, 5), enable_render=enable_render)





# class MazeEnvSample3x3(MazeEnv):

#     def __init__(self, enable_render=True):
#         super(MazeEnvSample3x3, self).__init__(maze_file="maze2d_3x3.npy", enable_render=enable_render)


# class MazeEnvRandom3x3(MazeEnv):

#     def __init__(self, enable_render=True):
#         super(MazeEnvRandom3x3, self).__init__(maze_size=(3, 3), enable_render=enable_render)


# class MazeEnvSample100x100(MazeEnv):

#     def __init__(self, enable_render=True):
#         super(MazeEnvSample100x100, self).__init__(maze_file="maze2d_100x100.npy", enable_render=enable_render)


# class MazeEnvRandom100x100(MazeEnv):

#     def __init__(self, enable_render=True):
#         super(MazeEnvRandom100x100, self).__init__(maze_size=(100, 100), enable_render=enable_render)

#Plus for q learning



# class MazeEnvRandom20x20Plus(MazeEnv):

#     def __init__(self, enable_render=True):
#         super(MazeEnvRandom20x20Plus, self).__init__(maze_size=(20, 20), mode="plus", enable_render=enable_render)


# class MazeEnvRandom30x30Plus(MazeEnv):
#     def __init__(self, enable_render=True):
#         super(MazeEnvRandom30x30Plus, self).__init__(maze_size=(30, 30), mode="plus", enable_render=enable_render)