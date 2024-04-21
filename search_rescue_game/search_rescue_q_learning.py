#q learning off policy - more than one policy, and model free
#TESTING~>~>~>~>~>~>~>>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~

import gymnasium
from . import envs
import numpy as np
import math
import random
from typing import Tuple
import sys


from gymnasium.wrappers import RecordVideo
from gymnasium.wrappers import RecordEpisodeStatistics


sys.path.append('/Users/smithnatalie/Desktop/dsan-6650-project')

#debugging
# print("Registered environments:", [spec.id for spec in gymnasium.envs.registry.values()])

###

#folder where we defined classes, map rendering, etc. 

#searchable learning rate and options:
#sources for using the max + decay with the log10 
#felt like i needed something more comprehensive than a list like [0.1, 0.2, ] etc
# https://github.com/monokim/PyRacing/blob/master/Pyrace_RL.py

def calc_learning_rate(t: int) -> float:
    #this code will allow us to search through multiple possible rates + decay of reward over time
    return max(0.2, min(0.8, 1.0 - math.log10((t + 1) / reward_decay)))

def calc_exploration_rate(t: int) -> float:
    return max(0.001, min(0.8, 1.0 - math.log10((t + 1) / reward_decay)))


if __name__ == "__main__":
    #create environment - this map will change depending on which want to select
    #start with a random generation
    env = gymnasium.make("map-random-10x10-v0", render_mode = "rgb_array")
    #debugging
    print("Render mode of the environment:", env.metadata.get('render_modes'))
    print("Environment metadata:", env.metadata)

    #screen recording
    recording_enabled = True
    
    #source for how to set up gymnasium record video and episode statistics
    # https://gymnasium.farama.org/main/api/wrappers/misc_wrappers/#gymnasium.wrappers.RecordVideo
    
    #recording every 10th episode -  used ChatGPT to help me do this
    # if recording_enabled:    
    #     print("Render modes from environment metadata:", env.metadata.get('render_modes'))       
    #     env = RecordVideo(env, video_folder='./game_recordings', episode_trigger=lambda x: x % 10 == 0, name_prefix="video")
    #     env = RecordEpisodeStatistics(env)
    
    print("Render mode of the environment before RecordVideo:", env.metadata.get('render_modes'))

    if recording_enabled:    
        env = RecordVideo(env, video_folder='./game_recordings', episode_trigger=lambda x: x % 100 == 0, name_prefix="video")

    map_size: Tuple[int,int] = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))

    #parameters: will change based on needs
    
    #training
    num_episodes: int = 100
    num_episode_steps: int = np.prod(map_size, dtype=int) * 100
    num_actions: int = env.action_space.n
    
    #learning
    reward_decay = float = np.prod(map_size, dtype=float) / 10.0
    learning_rate: float = calc_learning_rate(0)
    exploration_rate: float = calc_exploration_rate(0)
    discount_factor: float = 0.99
    
    
    #Q values
    Q: np.ndarray = np.zeros(map_size + (num_actions,), dtype=float)
    
    for episode in range(num_episodes):
        total_reward: int = 0
        #reset
        #debugging
        # observation = env.reset()
        observation, info = env.reset()
        
        #debugging
        # current_state = tuple(current_state[0])
        # current_state: Tuple[int,int] = tuple(observation)
        current_state = tuple(observation)
        
        #rendering after observation
        # env.render(mode="human")
        
        
        # how the dog agent will select the action to take next
        
        for episode_step in range(num_episode_steps):
            #random action based on exploration rate
            if random.uniform(0,1) < exploration_rate:
                # action: int = env.action_space.sample()
                action = int(env.action_space.sample())
            else:
                #otherwise, take a past action that was determined to yield best results (argmax)
                # action: int = int(np.argmax(Q[current_state]))
                action = int(np.argmax(Q[current_state]))
                
                
            #DEBUGGING
            # print("Current state", current_state)
            # print("q table shape", Q.shape)
            
            #going back to what was defined in forest_env for step function
            #should require 5 inputs
            
            #debugging
            print(f"Attempting to execute action: {action}, Type: {type(action)}")

            
            observation, reward, terminated, truncated, _ = env.step(action)
            
            total_reward += reward
            
            #go to next state
            next_state = tuple(observation)
            
            #temporal difference error
            # (reward+discountfactorgamma(Q[next_state]))−Q[current_state,action]
            
            TD: float = reward + discount_factor * np.amax(Q[next_state]) - Q[current_state + (action,)]

            #bellman equation
            Q[current_state + (action,)] +- learning_rate * TD
            current_state = next_state
            
            #render again after env moves into next state
            # env.render(mode="human")
            
            #end of game - reaches goal - terminated = true
            if terminated:
                print("Episode %d/%d complete after %d steps. Total reward = %f." % (episode + 1, num_episodes, episode_step + 1, total_reward))
                break
            #if reach max steps without goal
            elif episode_step >= num_episode_steps - 1:
                print("Episode %d/%d timed out after %d steps. Total reward = %f."
                      % (episode + 1, num_episodes, episode_step + 1, total_reward))
                
        
        #updating parameters
        exploration_rate = calc_exploration_rate(episode)
        learning_rate = calc_learning_rate(episode)
        
    env.close()
                
#~>~>~>~>~>~>~>>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~