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

import matplotlib.pyplot as plt

from search_rescue_game.envs.forest_env import MapEnv

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
    env.seed(101)
    #debugging
    print("Render mode of the environment:", env.metadata.get('render_modes'))
    print("Environment metadata:", env.metadata)

    #screen recording
    recording_enabled = True
    
    #source for how to set up gymnasium record video and episode statistics
    # https://gymnasium.farama.org/main/api/wrappers/misc_wrappers/#gymnasium.wrappers.RecordVideo
    
    #recording every 10th episode -  used ChatGPT to help me do this
    
    print("Render mode of the environment before RecordVideo:", env.metadata.get('render_modes'))

    if recording_enabled:
        
        #change modulo depending on number of episodes    
        # env = RecordVideo(env, video_folder='./game_recordings', episode_trigger=lambda x: x % 10 == 0, name_prefix="video")
        env = RecordVideo(env, video_folder='./game_recordings', episode_trigger=lambda x: x % 100 == 0, name_prefix="video")

    map_size: Tuple[int,int] = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))

    #parameters: will change based on needs
    
    #training
    
    #change number of episodes to capture diff metrics
    # num_episodes: int = 50
    num_episodes: int = 500
    
    
    num_episode_steps: int = np.prod(map_size, dtype=int) * 100
    num_actions: int = env.action_space.n
    
    #learning
    reward_decay = float = np.prod(map_size, dtype=float) / 10.0
    learning_rate: float = calc_learning_rate(0)
    exploration_rate: float = calc_exploration_rate(0)
    discount_factor: float = 0.99
    
    
    #Q values
    # Q: np.ndarray = np.zeros(map_size + (num_actions,), dtype=float)
    Q = np.zeros(map_size + (num_actions,), dtype=float)
    
    rewards = []
    
    #adding episode steps
    steps_per_episode = []
    
    for episode in range(num_episodes):
        total_reward = 0
        observation, info = env.reset()
        current_state = tuple(observation)

        for episode_step in range(num_episode_steps):
            # how the dog agent will select the action to take next
            # random action based on exploration rate 
            action = int(env.action_space.sample()) if random.uniform(0,1) < exploration_rate else int(np.argmax(Q[current_state]))
            
            #going back to what was defined in forest_env for step function
            #should require 5 inputs
            observation, reward, terminated, truncated, _  = env.step(action)
            
            total_reward += reward
            
            #go to next state
            next_state = tuple(observation)
            
            #temporal difference error
            TD = reward + discount_factor * np.amax(Q[next_state]) - Q[current_state + (action,)]
            
            #bellman equation :-)
    
            Q[current_state + (action,)] += learning_rate * TD
            
            current_state = next_state
            
            #end of game - reaches goal - terminated = true
            if terminated:
                print(f"Episode {episode + 1}/{num_episodes} complete after {episode_step + 1} steps. Total reward = {total_reward}.")
                steps_per_episode.append(episode_step + 1) #record steps
                break
            #if reach max steps without goal
            elif episode_step >= num_episode_steps - 1:
                print(f"Episode {episode + 1}/{num_episodes} timed out after {episode_step + 1} steps. Total reward = {total_reward}.")
                steps_per_episode.append(episode_step + 1)
        
        #updating parameters
        rewards.append(total_reward)
        exploration_rate = calc_exploration_rate(episode)
        learning_rate = calc_learning_rate(episode)
        
    env.close()
                
                
#Plotting Rewards

# plt.plot(rewards)
# plt.title('Total Rewards per Episode')
# plt.xlabel('Episode')
# plt.ylabel('Total Reward')
# plt.show()
#~>~>~>~>~>~>~>>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~

import json
with open('tabular_q_rewards.json', 'w') as f:
    json.dump(rewards, f)
with open('tabular_q_steps.json', 'w') as f:
    json.dump(steps_per_episode, f)

