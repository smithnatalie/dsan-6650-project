from gymnasium.envs.registration import register

#registering map formats so we can access later for games

register(
    id='map-10x10-v0',
    entry_point='search_rescue_game.envs.forest_env:MapEnv10x10',
    max_episode_steps=10000,
)

register(
    id='map-random-10x10-v0',
    entry_point='search_rescue_game.envs.forest_env:RandomMapEnv10x10',
    max_episode_steps=10000,
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
