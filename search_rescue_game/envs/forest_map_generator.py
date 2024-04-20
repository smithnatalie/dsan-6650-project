import os
# from search_rescue_game.envs.forest_view import Maps
from forest_view import Maps


if __name__ == "__main__":
    
    #check that map_options exists in cwd
    map_folder_path = './search_rescue_game/envs'
    dir_name = os.path.join(map_folder_path, "map_options")
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    #may remove or change option
    #create new map by incrementing to play unique map state games - starting with 100 possible map options
    map_path = None
    for i in range(1, 100):
        map_name = "map_%03d.npy" % i
        map_path = os.path.join(dir_name, map_name)
        if not os.path.exists(map_path):
            break
        if i == 99:
            raise ValueError("Total number of possible maps in directory (100) exceeded.")
        
    maps = Maps(map_size=(10,10))
    maps.save_map(map_path)
    print("A new map has been generated. It is located at %s." % map_path)