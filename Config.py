## Created by : Sumudu Madushanka
## Last update : 8/10/2020

import json
from log import log_write

### Configurations ###
# Load the configurations
def load_configs(config_file_name):
    try:
        log_write("Loading Configurations...\n")
        config_file = open(config_file_name, "r")
        config_file.close()
        
    except FileNotFoundError:
        log_write("Config File Not Found.\n")
        log_write("Creating config file...\n")
        
        configs = {}
        configs["Colour"] = {"White" : (255, 255, 255),
                             "Black" : (0, 0, 0),
                             "Yellow" : (255, 255, 0),
                             "LightYellow" : (255, 255, 224),
                             "Red" : (255, 0, 0),
                             "Green" : (0, 255, 0),
                             "LightGreen" : (144, 238, 144),
                             "DarkGreen" : (0, 100, 0),
                             "Blue" : (0, 0, 255),
                             "LightBlue" : (173, 216, 230),
                             "DarkBlue" : (0, 0, 139)}
        configs["Font"] = {"Size" : 30}
        configs["Snake"] = {"Block" : 10}
        configs["Display"] = {"Width" : 600,
                              "Height" : 400 + configs["Font"]["Size"]}
        configs["Game"] = {"Type" : 0,
                           "Level" : 3,
                           "Type_List" : ["No Barrier", "Box Barrier", "Tunnel", "Rail", "Mill"],
                           "Colour_Code" : [
                               {
                                   "Snake" : "Black",
                                   "Food" : "Green",
                                   "Type" : "Blue",
                                   "Score" : "Green",
                                   "Background" : "White"
                               },
                               {
                                   "Snake" : "Black",
                                   "Food" : "Green",
                                   "Type" : "Blue",
                                   "Score" : "Green",
                                   "Background" : "LightYellow",
                                   "Barrier" : "Red"
                               },
                               {
                                   "Snake" : "Red",
                                   "Food" : "Yellow",
                                   "Type" : "Black",
                                   "Score" : "Yellow",
                                   "Background" : "LightGreen",
                                   "Barrier" : "DarkBlue"
                               },
                               {
                                   "Snake" : "Green",
                                   "Food" : "Yellow",
                                   "Type" : "LightYellow",
                                   "Score" : "Yellow",
                                   "Background" : "Black",
                                   "Barrier" : "Red"
                               },
                               {
                                   "Snake" : "DarkBlue",
                                   "Food" : "Yellow",
                                   "Type" : "Black",
                                   "Score" : "Yellow",
                                   "Background" : "LightGreen",
                                   "Barrier" : "DarkGreen"
                               }
                           ]}
        
        config_file = open(config_file_name, "w")
        json.dump(configs, config_file, indent = 4)
        config_file.close()
        
        log_write("Config File Create completed\n")
        
    finally:
        config_file = open(config_file_name,)
        configs = json.load(config_file)
        config_file.close()

    log_write("Load Configurations Completed\n")

    return configs

# Change the Config file
def change_configs(config_file_name, configs):
    config_file = open(config_file_name, "w")
    json.dump(configs, config_file, indent = 4)
    config_file.close()

    log_write("Changed the configurations\n")
