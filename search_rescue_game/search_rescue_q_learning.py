#q learning off policy - more than one policy, and model free
#TESTING~>~>~>~>~>~>~>>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~

import numpy as np
import math
import random
from typing import Tuple

import gymnasium
from gymnasium.wrappers import RecordVideo, RecordEpisodeStatistics
import envs

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
    env = gymnasium.make("map-random-10x10-v0")
    
    #screen recording
    recording_enabled = False
    
    #source for how to set up gymnasium record video and episode statistics
    # https://gymnasium.farama.org/main/api/wrappers/misc_wrappers/#gymnasium.wrappers.RecordVideo
    
    if recording_enabled:
        env = RecordVideo(env, video_folder='./game_recordings', episode_trigger=lambda x: True, name_prefix="video")
        env = RecordEpisodeStatistics(env)

    map_size: Tuple[int,int] = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))

    #parameters: will change based on needs
    
    #training
    num_episodes: int = 50
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
        observation = env.reset()
        
        current_state: Tuple[int,int] = tuple(observation)
        
        #rendering after observation
        env.render(mode="human")
        
        # how the dog agent will select the action to take next
        
        for episode_step in range(num_episode_steps):
            #random action based on exploration rate
            if random.uniform(0,1) < exploration_rate:
                action: int = env.action_space.sample()
            else:
                #otherwise, take a past action that was determined to yield best results (argmax)
                action: int = int(np.argmax(Q[current_state]))
            
            #going back to what was defined in forest_env for step function
            #should require 5 inputs    
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
            env.render(mode="human")
            
            #end of game - terminated = true
            if terminated:
                print("Episode %d/%d complete after %d steps. Total reward = %f." % (episode + 1, num_episodes, episode_step + 1, total_reward))
                break
            #if issue arises/timeout
            elif episode_step >= num_episode_steps - 1:
                print("Episode %d/%d timed out after %d steps. Total reward = %f."
                      % (episode + 1, num_episodes, episode_step + 1, total_reward))
                
        
        #updating parameters
        exploration_rate = calc_exploration_rate(episode)
        learning_rate = calc_learning_rate(episode)
        
    env.close()
                
    
    
    
    
#~>~>~>~>~>~>~>>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~>~




# import sys
# import numpy as np
# import math
# import random

# import gymnasium
# from gymnasium.wrappers import RecordVideo, RecordEpisodeStatistics


# from search_rescue_game import envs

# #source : https://gymnasium.farama.org/main/introduction/record_agent/



# def simulate():
#     learning_rate = get_learning_rate(0)
#     explore_rate = get_explore_rate(0)
#     discount_factor = 0.99

#     num_streaks = 0

#     env.render()

#     for episode in range(NUM_EPISODES):

#         obv, _ = env.reset()

#         #initial state
#         state_0 = state_to_bucket(obv)
#         total_reward = 0

#         for t in range(MAX_T):

#             # Select an action
#             action = select_action(state_0, explore_rate)

#             # execute the action
#             # obv, reward, done, _ = env.step(action)
            
#             #to deal with gymnasium updated documentation: https://stackoverflow.com/questions/73195438/openai-gyms-env-step-what-are-the-values
            
#             obv, reward, truncated, terminated, info = env.step(action)
#             done = truncated or terminated
            
#             print(info)
            
#             # Observe the result
#             state = state_to_bucket(obv)
#             total_reward += reward

#             # Update the Q based on the result
#             best_q = np.amax(q_table[state])
#             q_table[state_0 + (action,)] += learning_rate * (reward + discount_factor * (best_q) - q_table[state_0 + (action,)])

#             # Setting up for the next iteration
#             state_0 = state
            
            

#             # Print data
#             if DEBUG_MODE == 2:
#                 print("\nEpisode = %d" % episode)
#                 print("t = %d" % t)
#                 print("Action: %d" % action)
#                 print("State: %s" % str(state))
#                 print("Reward: %f" % reward)
#                 print("Best Q: %f" % best_q)
#                 print("Explore rate: %f" % explore_rate)
#                 print("Learning rate: %f" % learning_rate)
#                 print("Streaks: %d" % num_streaks)
#                 print("")

#             elif DEBUG_MODE == 1:
#                 if done or t >= MAX_T - 1:
#                     print("\nEpisode = %d" % episode)
#                     print("t = %d" % t)
#                     print("Explore rate: %f" % explore_rate)
#                     print("Learning rate: %f" % learning_rate)
#                     print("Streaks: %d" % num_streaks)
#                     print("Total reward: %f" % total_reward)
#                     print("")

#             # Render tha maze
#             if RENDER_MAZE:
#                 env.render()

#             # if env.is_game_over():
#             if env.unwrapped.is_game_over():
#                 sys.exit()

#             if done:
#                 print("Episode %d finished after %f time steps with total reward = %f (streak %d)."
#                       % (episode, t, total_reward, num_streaks))

#                 if t <= SOLVED_T:
#                     num_streaks += 1
#                 else:
#                     num_streaks = 0
#                 break

#             elif t >= MAX_T - 1:
#                 print("Episode %d timed out at %d with total reward = %f."
#                       % (episode, t, total_reward))

#         # It's considered done when it's solved over 120 times consecutively
#         if num_streaks > STREAK_TO_END:
#             break

#         # Update parameters
#         explore_rate = get_explore_rate(episode)
#         learning_rate = get_learning_rate(episode)
        
        
        
# def select_action(state, explore_rate):
#     # Select a random action
#     if random.random() < explore_rate:
#         action = env.action_space.sample()
#     # Select the action with the highest q
#     else:
#         action = int(np.argmax(q_table[state]))
#     return action


# def get_explore_rate(t):
#     return max(MIN_EXPLORE_RATE, min(0.8, 1.0 - math.log10((t+1)/DECAY_FACTOR)))

# def get_learning_rate(t):
#     return max(MIN_LEARNING_RATE, min(0.8, 1.0 - math.log10((t+1)/DECAY_FACTOR)))


# def state_to_bucket(state):
#     bucket_indice = []
#     for i in range(len(state)):
#         if state[i] <= STATE_BOUNDS[i][0]:
#             bucket_index = 0
#         elif state[i] >= STATE_BOUNDS[i][1]:
#             bucket_index = NUM_BUCKETS[i] - 1
#         else:
#             # Mapping the state bounds to the bucket array
#             bound_width = STATE_BOUNDS[i][1] - STATE_BOUNDS[i][0]
#             offset = (NUM_BUCKETS[i]-1)*STATE_BOUNDS[i][0]/bound_width
#             scaling = (NUM_BUCKETS[i]-1)/bound_width
#             bucket_index = int(round(scaling*state[i] - offset))
#         bucket_indice.append(bucket_index)
#     return tuple(bucket_indice)


# if __name__ == "__main__":

#     # Initialize the "maze" environment
#     # tmp_env = gymnasium.make("random-forest-map-plus-10x10-v0", render_mode = "rgb_array")
#     tmp_env = gymnasium.make("custom-forest-map-10x10-v0", render_mode = "rgb_array")

#     env = gymnasium.wrappers.RecordVideo(env=tmp_env, video_folder="./game_recordings", name_prefix="test-video", episode_trigger=lambda x: x % 2 == 0)

#     observation, info = env.reset()

#     '''
#     Defining the environment related constants
#     '''
#     # Number of discrete states (bucket) per state dimension
#     MAZE_SIZE = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))
#     NUM_BUCKETS = MAZE_SIZE  # one bucket per grid

#     # Number of discrete actions
#     NUM_ACTIONS = env.action_space.n  # ["N", "S", "E", "W"]
#     # Bounds for each discrete state
#     STATE_BOUNDS = list(zip(env.observation_space.low, env.observation_space.high))

#     '''
#     Learning related constants
#     '''
#     MIN_EXPLORE_RATE = 0.001
#     MIN_LEARNING_RATE = 0.2
#     DECAY_FACTOR = np.prod(MAZE_SIZE, dtype=float) / 10.0

#     '''
#     Defining the simulation related constants
#     '''
#     NUM_EPISODES = 50000
#     MAX_T = np.prod(MAZE_SIZE, dtype=int) * 100
#     STREAK_TO_END = 100
#     SOLVED_T = np.prod(MAZE_SIZE, dtype=int)
#     DEBUG_MODE = 0
#     RENDER_MAZE = True
#     ENABLE_RECORDING = True

#     '''
#     Creating a Q-Table for each state-action pair
#     '''
#     q_table = np.zeros(NUM_BUCKETS + (NUM_ACTIONS,), dtype=float)

#     '''
#     Begin simulation
#     '''
 
    
#     env.start_video_recorder()
    
#     simulate()
    
#     env.close_video_recorder()
    
#     env.close()