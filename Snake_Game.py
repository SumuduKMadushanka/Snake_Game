## Created by : Sumudu Madushanka
## Last update : 8/4/2020

from log import *
from Config import *
from Message import *
from Basic_game_functions import change_game_type, change_game_level, high_score
import pygame

init_log_file()
log_write("Import basic game funcrions\n")

config_file_name = "Config.json"
configs = load_configs(config_file_name)

pygame.init()

log_write("pygame init completed\n")
log_write("Start Global Variables init...\n")

### Global Variables ###
# Display
dis_width = configs["Display"]["Width"]
dis_height = configs["Display"]["Height"]
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake Game")

log_write("Display init completed\n")

# Colours
white = configs["Colour"]["White"]
green = configs["Colour"]["Green"]
blue = configs["Colour"]["Blue"]

log_write("Colour Init Completed\n")

# Font
font_size = configs["Font"]["Size"]

log_write("Font Init Completed\n")

#Clock 
clock = pygame.time.Clock()

log_write("Clock init completed\n")
log_write("Global Variables init completed\n")

### Main Function ###
def main_loop():
    log_write("Start Init Game variables...\n")
    # Basic Variables
    game_over = False
    select_item = 0
    log_write("Init Game variables Completed\n")

    while not game_over:
        dis.fill(white)
        message(dis, font_size, "Snake Game", green, white, dis_width//3, ((dis_height - font_size)//3 + font_size))
        item_list = ["Start Game", "Game Type", "Level", "High Score", "Quit Game"]
        for i in range(len(item_list)):
            if (select_item == i):
                f_colour = white
                bg_colour = blue
            else:
                f_colour = blue
                bg_colour = white
            message(dis, font_size, item_list[i], f_colour, bg_colour, dis_width//3, ((dis_height - font_size)//3 + ((2 + i) * font_size)))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log_write("Quit the Game\n")
                game_over = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    tmp = select_item - 1
                    select_item = ((len(item_list) - 1) if tmp < 0 else tmp)
                elif event.key == pygame.K_DOWN:
                    tmp = select_item + 1
                    select_item = (0 if tmp > (len(item_list) - 1) else tmp)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    log_write("Select " + item_list[select_item] + "\n")
                    if select_item == (len(item_list) - 1):
                        game_over = True
                    elif select_item == 0:
                        if configs["Game"]["Type"] == 0:
                            import No_barrier
                            No_barrier.game_loop_no_barrier(dis, configs, clock)
                        elif configs["Game"]["Type"] == 1:
                            import Box_barrier
                            Box_barrier.game_loop_box_barrier(dis, configs, clock)
                        elif configs["Game"]["Type"] == 2:
                            import Tunnel
                            Tunnel.game_loop_tunnel(dis, configs, clock)
                    elif select_item == 1:
                        change_game_type(dis, configs, config_file_name)
                    elif select_item == 2:
                        change_game_level(dis, configs, config_file_name)
                    elif select_item == 3:
                        high_score(dis, configs["Game"]["Type"], white, blue, font_size, dis_width, dis_height)
                        
    log_write("Quiting the Game...\n")
    pygame.quit()
    log_write("Game Quit\n")

log_write("Starting Game...\n")

main_loop()
log_write("Game finished\n")
log_write("Log finished\n")
quit()
