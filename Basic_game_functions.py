## Created by : Sumudu Madushanka
## Last update : 8/4/2020

import pygame
from log import log_write
from Message import message
from Config import change_configs

### Basic Game Functions ###
# Change the game type
def change_game_type(dis, configs, config_file_name):
    select_item = configs["Game"]["Type"]
    change_item = False
    while not change_item:
        dis.fill(configs["Colour"]["White"])
        message(dis, configs["Font"]["Size"], "Game Type", configs["Colour"]["Green"], configs["Colour"]["White"], configs["Display"]["Width"]/3, ((configs["Display"]["Height"] - configs["Font"]["Size"])/3 + configs["Font"]["Size"]))
        item_list = ["No Barrier", "Box Barrier"]
        for i in range(len(item_list)):
            if (select_item == i):
                f_colour = configs["Colour"]["White"]
                bg_colour = configs["Colour"]["Blue"]
            else:
                f_colour = configs["Colour"]["Blue"]
                bg_colour = configs["Colour"]["White"]
            message(dis, configs["Font"]["Size"], item_list[i], f_colour, bg_colour, configs["Display"]["Width"]/3, ((configs["Display"]["Height"] - configs["Font"]["Size"])/3 + ((2 + i) * configs["Font"]["Size"])))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                change_item = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    tmp = select_item - 1
                    select_item = ((len(item_list) - 1) if tmp < 0 else tmp)
                elif event.key == pygame.K_DOWN:
                    tmp = select_item + 1
                    select_item = (0 if tmp > (len(item_list) - 1) else tmp)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    log_write("Select " + item_list[select_item] + "\n")
                    if select_item != configs["Game"]["Type"]:
                        configs["Game"]["Type"] = select_item
                        change_configs(config_file_name, configs)
                    change_item = True

# Change the game level
def change_game_level(dis, configs, config_file_name):
    level = configs["Game"]["Level"]
    changed = False
    while not changed:
        dis.fill(configs["Colour"]["White"])
        message(dis, configs["Font"]["Size"], "Game Level " + str(level), configs["Colour"]["Green"], configs["Colour"]["White"], configs["Display"]["Width"]//3, ((configs["Display"]["Height"] - configs["Font"]["Size"])//3 + configs["Font"]["Size"]))
        pygame.draw.rect(dis, configs["Colour"]["Blue"], [configs["Display"]["Width"]//3, ((configs["Display"]["Height"] - configs["Font"]["Size"])//3 + (2 * configs["Font"]["Size"])), 25 * level, 20])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                changed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_RIGHT:
                    level = min(level + 1, 5)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_LEFT:
                    level = max(level - 1, 1)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    log_write("Level " + str(level) + "\n")
                    if level != configs["Game"]["Level"]:
                        configs["Game"]["Level"] = level
                        change_configs(config_file_name, configs)
                    changed = True

# Show High score
def high_score(dis, game_type, bg_color, font_color, font_size, dis_width, dis_height):
    show = True
    score_file_name = ("high_score_no_barrier.txt" if game_type == 0 else "high_score_box_barrier.txt")
    while show:
        dis.fill(bg_color)
        try:
            score_file = open(score_file_name, "r")
            high_score = int(score_file.read())
            score_file.close()
        except IOError:
            high_score = 0

        message(dis, font_size, "High Score : " + str(high_score), font_color, bg_color, dis_width/3, (dis_height - font_size)/3)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER)):
                show = False

# Draw the snake
def draw_snake(dis, snake_block, snake_list, Snake_colour):
    for cordinate in snake_list:
        pygame.draw.rect(dis, Snake_colour, [cordinate[0], cordinate[1], snake_block, snake_block])
        
