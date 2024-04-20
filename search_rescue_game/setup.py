from setuptools import setup

setup(name="envs",
      version="0.1",
      url="https://github.com/smithnatalie/dsan-6650-project",
      author="Natalie Smith",
      packages=["search_rescue_game", "search_rescue_game.envs"],
      package_data= {
          "search_rescue_game.envs" : ["map_options/*.npy"]
      },
      install_requires = ["gymnasium", "numpy", "pygame"]
    )