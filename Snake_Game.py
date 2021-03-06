## Created by : Sumudu Madushanka
## Last update : 9/25/2020

from log import *
from Config import *
from Message import *
from Basic_game_functions import select_function
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
    item_list = ["Start Game", "Game Type", "Level", "High Score", "Quit Game"]
    select_item = 0
    log_write("Init Game variables Completed\n")

    while not game_over:
        dis.fill(white)
        message(dis, (2 * font_size), "Snake Game", green, white, dis_width//4, (dis_height - font_size)//4)
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
                break
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    tmp = select_item - 1
                    select_item = ((len(item_list) - 1) if tmp < 0 else tmp)
                    break
                elif event.key == pygame.K_DOWN:
                    tmp = select_item + 1
                    select_item = (0 if tmp > (len(item_list) - 1) else tmp)
                    break
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    log_write("Select " + item_list[select_item] + "\n")
                    if select_item == (len(item_list) - 1):
                        game_over = True
                    else:
                        select_function(dis, select_item, configs, config_file_name, clock)
                    break
            elif event.type == pygame.MOUSEMOTION:
                m_pos = pygame.mouse.get_pos()
                m_pos_x = m_pos[0]
                m_pos_y = m_pos[1]
                if (m_pos_x > 200) and (m_pos_x < 310):
                    i = (m_pos_y - 190)//30
                    if i >= 0 and i < len(item_list):
                        select_item = i
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                m_clicked = pygame.mouse.get_pressed()
                if m_clicked == (1, 0, 0):
                    m_pos = pygame.mouse.get_pos()
                    m_pos_x = m_pos[0]
                    m_pos_y = m_pos[1]
                    if (m_pos_x > 200) and (m_pos_x < 310) and (m_pos_y > 190) and (m_pos_y < (190 + len(item_list) * 30)):
                        log_write("Select " + item_list[select_item] + "\n")
                        if select_item == (len(item_list) - 1):
                            game_over = True
                        else:
                            select_function(dis, select_item, configs, config_file_name, clock)
                break
        pygame.event.clear()
                        
    log_write("Quiting the Game...\n")
    pygame.quit()
    log_write("Game Quit\n")

log_write("Starting Game...\n")

main_loop()
log_write("Game finished\n")
log_write("Log finished\n")
quit()
