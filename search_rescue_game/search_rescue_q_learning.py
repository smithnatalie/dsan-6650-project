import sys
import numpy as np
import math
import random

import gymnasium
from gymnasium.wrappers import RecordVideo, RecordEpisodeStatistics


from search_rescue_game import envs

#source : https://gymnasium.farama.org/main/introduction/record_agent/

def main(ENABLE_RECORDING, NUM_EPISODES, MAX_T):
    env = gymnasium.make("random-forest-map-plus-10x10-v0", render_mode='rgb_array')
    video_folder = './game_recordings'
    
    if ENABLE_RECORDING:
        env = RecordVideo(env, video_folder=video_folder, episode_trigger=lambda x: True, name_prefix="random-forest-map-plus")

    # Initialize constants and Q-table
    MAP_SIZE = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))
    NUM_BUCKETS = MAP_SIZE
    NUM_ACTIONS = env.action_space.n
    STATE_BOUNDS = list(zip(env.observation_space.low, env.observation_space.high))

    q_table = np.zeros(NUM_BUCKETS + (NUM_ACTIONS,), dtype=float)

    simulate(env, NUM_EPISODES, q_table, STATE_BOUNDS, NUM_BUCKETS)
    
    return env



def simulate(env, num_episodes, q_table, state_bounds, num_buckets):
    MIN_EXPLORE_RATE = 0.001
    MIN_LEARNING_RATE = 0.2
    DECAY_FACTOR = np.prod(num_buckets, dtype=float) / 10.0


    for episode in range(num_episodes):
        learning_rate = get_learning_rate(episode, DECAY_FACTOR, MIN_LEARNING_RATE)
        explore_rate = get_explore_rate(episode, DECAY_FACTOR, MIN_EXPLORE_RATE)

        obv = env.reset()
        state_0 = state_to_bucket(obv, state_bounds, num_buckets)
        total_reward = 0

        for t in range(MAX_T):
            action = select_action(state_0, explore_rate, q_table)
            obv, reward, done, _ = env.step(action)
            state = state_to_bucket(obv, state_bounds, num_buckets)

            best_q = np.amax(q_table[state])
            q_table[state_0 + (action,)] += learning_rate * (reward + discount_factor * best_q - q_table[state_0 + (action,)])

            state_0 = state
            total_reward += reward

            if done or env.is_game_over():
                break
            
# def state_to_bucket(state, state_bounds, num_buckets):
#     if any(x is None for x in state):
#         raise ValueError(f"Invalid state received: {state}")
    
#     if not isinstance(state, np.ndarray) or state.ndim != 1:
#         raise ValueError(f"State must be a 1D numpy array, got {type(state)} with shape {state.shape}")
    
#     bucket_indice = []
    
#     for i in range(len(state)):
#         bound_width = state_bounds[i][1] - state_bounds[i][0]
#         offset = (num_buckets[i]-1) * state_bounds[i][0] / bound_width
#         scaling = (num_buckets[i]-1) / bound_width
        
#         #calculate result
#         result = scaling * state[i] - offset
#         bucket_index = int(np.round(result))
#         bucket_indice.append(bucket_index)
        
#     return tuple(bucket_indice)

def state_to_bucket(state, state_bounds, num_buckets):
    try:
        # Convert state to a numpy array of type int, ensure it's flat
        if not isinstance(state, np.ndarray) or state.ndim != 1:
            state = np.array(state, dtype=int).flatten()
    except Exception as e:
        raise ValueError(f"Failed to convert state to a proper numpy array: {e}")

    bucket_indices = []
    for i in range(len(state)):
        bound_width = state_bounds[i][1] - state_bounds[i][0]
        offset = (num_buckets[i]-1) * state_bounds[i][0] / bound_width
        scaling = (num_buckets[i]-1) / bound_width
        bucket_index = int(np.round(scaling * state[i] - offset))
        bucket_indices.append(bucket_index)

    return tuple(bucket_indices)




           
# def state_to_bucket(state, state_bounds, num_buckets):
#     if any(x is None for x in state):
#         raise ValueError(f"Invalid state received: {state}")
#     if isinstance(state, np.ndarray) and state.ndim > 1:
#         raise ValueError(f"state array should be 1-d, received shape: {state.shape}")
#     bucket_indice = []
#     for i in range(len(state)):
#         bound_width = state_bounds[i][1] - state_bounds[i][0]
#         offset = (num_buckets[i]-1) * state_bounds[i][0] / bound_width
#         scaling = (num_buckets[i]-1) / bound_width
        
#         #debug info
#         print(f"processing state[{i}]: {state[i]}, scaling: {scaling}, offset: {offset}")
        
#         #used chatgpt to assist with fixing bucket index - was totally lost here
#         # bucket_index = int(round(scaling * state[i] - offset))
#         result = scaling * state[i] - offset
#         if isinstance(result, np.ndarray) and result.size == 1:
#             bucket_index = int(np.round(result).item())
#         elif isinstance(result, (float, np.floating)):
#             bucket_index = int(round(result))
#         else:
#             raise ValueError(f"result is not a scalar: result={result}, type={type(result)}")    
#         #bucket_index = int(np.round(scaling * state[i] - offset).item())

#         bucket_indice.append(bucket_index)
#     return tuple(bucket_indice)


def get_explore_rate(t, decay_factor, min_explore_rate):
    return max(min_explore_rate, min(0.8, 1.0 - math.log10((t + 1) / decay_factor)))

def get_learning_rate(t, decay_factor, min_learning_rate):
    return max(min_learning_rate, min(0.8, 1.0 - math.log10((t + 1) / decay_factor)))

def select_action(state, explore_rate, q_table):
    if random.random() < explore_rate:
        return env.action_space.sample()
    else:
        return int(np.argmax(q_table[state]))


if __name__ == "__main__":
    ENABLE_RECORDING = True
    NUM_EPISODES = 5  #50000
    MAX_T = 1000
    env = None
    try:
        env = main(ENABLE_RECORDING, NUM_EPISODES, MAX_T)

    finally:
        if env is not None:
            env.close()
    # main()
    
# def simulate():

#     # Instantiating the learning related parameters
#     learning_rate = get_learning_rate(0)
#     explore_rate = get_explore_rate(0)
#     discount_factor = 0.99

#     num_streaks = 0

#     # Render tha maze
#     env.render()

#     for episode in range(NUM_EPISODES):

#         # Reset the environment
#         obv = env.reset()

#         # the initial state
#         state_0 = state_to_bucket(obv)
#         total_reward = 0

#         for t in range(MAX_T):

#             # Select an action
#             action = select_action(state_0, explore_rate)

#             # execute the action
#             obv, reward, done, _ = env.step(action)

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

#             if env.is_game_over():
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

#     #initialize env
#     env = gymnasium.make("maze-random-10x10-plus-v0")
    
#     #recordings
#     recording_folder = "./game_recordings"
#     if ENABLE_RECORDING:
#         # env.monitor.start(recording_folder, force=True)
#         env = RecordVideo(env, video_folder=recording_folder, episode_trigger=capped_cubic_video_schedule)
    

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

   
#     #Learning related constants
 
#     MIN_EXPLORE_RATE = 0.001
#     MIN_LEARNING_RATE = 0.2
#     DECAY_FACTOR = np.prod(MAZE_SIZE, dtype=float) / 10.0


#     #Simulation related constants

#     NUM_EPISODES = 50000
#     MAX_T = np.prod(MAZE_SIZE, dtype=int) * 100
#     STREAK_TO_END = 100
#     SOLVED_T = np.prod(MAZE_SIZE, dtype=int)
#     DEBUG_MODE = 0
#     RENDER_MAZE = True
#     # ENABLE_RECORDING = True

    
#     #q table for each state-action pair
#     q_table = np.zeros(NUM_BUCKETS + (NUM_ACTIONS,), dtype=float)

  
#     #simulation


    # simulate()

    # if ENABLE_RECORDING:
    #     env.monitor.close()