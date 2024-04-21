from gymnasium.envs.registration import register

#registering map formats so we can access later for games

#TESTING#################################################

register(
    id='map-10x10-v0',
    entry_point='search_rescue_game.envs.forest_env:MapEnv10x10',
    max_episode_steps=10000,
)

register(
    id='map-random-10x10-v0',
    entry_point='search_rescue_game.envs.forest_env:RandomMapEnv10x10',
    max_episode_steps=10000
)

register(
    id='map-25x25-v0',
    entry_point='search_rescue_game.envs.forest_env:MapEnv25x25',
    max_episode_steps=70000,
)

register(
    id='map-random-25x25-v0',
    entry_point='search_rescue_game.envs.forest_env:RandomMapEnv25x25',
    max_episode_steps=70000
)

#TESTING#################################################


# register(
#     id='forest-map-10x10-v0',
#     entry_point='search_rescue_game.envs:ForestMap10x10',
#     max_episode_steps=10000,#may change steps
# )

# register(
#     id='random-forest-map-10x10-v0',
#     entry_point='search_rescue_game.envs:RandomForestMap10x10',
#     max_episode_steps=10000,
#     nondeterministic=True,
# )


# register(
#     id='random-forest-map-plus-10x10-v0',
#     entry_point='search_rescue_game.envs:RandomForestMap10x10Plus',
#     max_episode_steps=1000000,
#     nondeterministic=True,
#     kwargs={'enable_render': True, 'render_mode': 'rgb_array'}
    
# )

# register(
#     id='custom-forest-map-10x10-v0',
#     entry_point='search_rescue_game.envs:CustomForestMap10x10',
#     max_episode_steps=1000000,
#     nondeterministic=True,
#     kwargs={'enable_render': True, 'render_mode': 'rgb_array', 'custom_map': True}
# )


# register(
#     id='maze-v0',
#     entry_point='gym_maze.envs:MazeEnvSample5x5',
#     max_episode_steps=2000,
# )

# register(
#     id='maze-sample-5x5-v0',
#     entry_point='gym_maze.envs:MazeEnvSample5x5',
#     max_episode_steps=2000,
# )

# register(
#     id='maze-random-5x5-v0',
#     entry_point='gym_maze.envs:MazeEnvRandom5x5',
#     max_episode_steps=2000,
#     nondeterministic=True,
# )

# register(
#     id='maze-sample-10x10-v0',
#     entry_point='gym_maze.envs:MazeEnvSample10x10',
#     max_episode_steps=10000,
# )

# register(
#     id='maze-random-10x10-v0',
#     entry_point='gym_maze.envs:MazeEnvRandom10x10',
#     max_episode_steps=10000,
#     nondeterministic=True,
# )

# register(
#     id='maze-sample-3x3-v0',
#     entry_point='gym_maze.envs:MazeEnvSample3x3',
#     max_episode_steps=1000,
# )

# register(
#     id='maze-random-3x3-v0',
#     entry_point='gym_maze.envs:MazeEnvRandom3x3',
#     max_episode_steps=1000,
#     nondeterministic=True,
# )


# register(
#     id='maze-sample-100x100-v0',
#     entry_point='gym_maze.envs:MazeEnvSample100x100',
#     max_episode_steps=1000000,
# )

# register(
#     id='maze-random-100x100-v0',
#     entry_point='gym_maze.envs:MazeEnvRandom100x100',
#     max_episode_steps=1000000,
#     nondeterministic=True,
# )

# register(
#     id='maze-random-10x10-plus-v0',
#     entry_point='gym_maze.envs:MazeEnvRandom10x10Plus',
#     max_episode_steps=1000000,
#     nondeterministic=True,
# )

# register(
#     id='maze-random-20x20-plus-v0',
#     entry_point='gym_maze.envs:MazeEnvRandom20x20Plus',
#     max_episode_steps=1000000,
#     nondeterministic=True,
# )

# register(
#     id='maze-random-30x30-plus-v0',
#     entry_point='gym_maze.envs:MazeEnvRandom30x30Plus',
#     max_episode_steps=1000000,
#     nondeterministic=True,
# )