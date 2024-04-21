import gymnasium

from search_rescue_game import envs

env = gymnasium.make('map-10x10-v0')

print("Registered environments:", [spec.id for spec in gymnasium.envs.registry.values()])

