## Created by : Sumudu Madushanka
## Last update : 12/7/2020

log_file = open("Snake_Game_Log.txt", "w")
log_file.write("Start import configparser, pygame, time and random\n")
log_file.close()

def log_write(log):
    log_file = open("Snake_Game_Log.txt", "a")
    log_file.write(log)
    log_file.close()

import json
import pygame
import time
import random

log_write("Import json, pygame, time and random packages completed\nStart init pygame\n")
log_write("Loading Configurations...\n")

try:
    config_file = open("Config.json", "r")
    config_file.close()
    
except FileNotFoundError:
    log_write("Config File Not Found.\nCreating config file...\n")
    
    configs = {}
    configs["Colour"] = {"White" : (255, 255, 255),
                         "Black" : (0, 0, 0),
                         "Yellow" : (255, 255, 0),
                         "Red" : (255, 0, 0),
                         "Green" : (0, 255, 0),
                         "Blue" : (0, 0, 255)}
    configs["Font"] = {"Size" : 30}
    configs["Snake"] = {"Block" : 10}
    configs["Display"] = {"Width" : 600,
                          "Height" : 400 + configs["Font"]["Size"]}
    configs["Game"] = {"Type" : 0,
                       "Level" : 3}
    
    config_file = open("Config.json", "w")
    json.dump(configs, config_file, indent = 4)
    config_file.close()
    
    log_write("Config File Create completed\n")
    
finally:
    config_file = open("Config.json",)
    configs = json.load(config_file)
    config_file.close()
    
log_write("Load Configurations Completed\n")

pygame.init()

log_write("pygame init completed\n")
log_write("Start Variables init\n")

### Global Variables ###
# Font
font_style = pygame.font.SysFont(None, configs["Font"]["Size"])

log_write("Font init completed\n")

# Display
dis = pygame.display.set_mode((configs["Display"]["Width"], configs["Display"]["Height"]))
pygame.display.set_caption("Snake Game")

log_write("Display init completed\n")

#Clock 
clock = pygame.time.Clock()

log_write("Clock init completed\n")
log_write("Variables init completed\n")
log_write("Start Define game funcrions\n")

### Game Functions ###
# Change the Config file
def change_configs():
    config_file = open("Config.json", "w")
    json.dump(configs, config_file, indent = 4)
    config_file.close()

    log_write("Changed the configurations\n")

# Draw the snake
def draw_snake(snake_block, snake_list, Snake_colour):
    for cordinate in snake_list:
        pygame.draw.rect(dis, Snake_colour, [cordinate[0], cordinate[1], snake_block, snake_block])

# Write a message on screen
def message(msg, colour, bg_colour, x, y):
    mesg = font_style.render(msg, True, colour, bg_colour)
    dis.blit(mesg, [int(x), int(y)])

# Change the game type
def change_game_type():
    select_item = configs["Game"]["Type"]
    change_item = False
    while not change_item:
        dis.fill(configs["Colour"]["White"])
        message("Game Type", configs["Colour"]["Green"], configs["Colour"]["White"], configs["Display"]["Width"]/3, ((configs["Display"]["Height"] - configs["Font"]["Size"])/3 + configs["Font"]["Size"]))
        item_list = ["No Barrier", "Box Barrier"]
        for i in range(len(item_list)):
            if (select_item == i):
                f_colour = configs["Colour"]["White"]
                bg_colour = configs["Colour"]["Blue"]
            else:
                f_colour = configs["Colour"]["Blue"]
                bg_colour = configs["Colour"]["White"]
            message(item_list[i], f_colour, bg_colour, configs["Display"]["Width"]/3, ((configs["Display"]["Height"] - configs["Font"]["Size"])/3 + ((2 + i) * configs["Font"]["Size"])))
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
                        change_configs()
                    change_item = True

# Change the game level
def change_game_level():
    level = configs["Game"]["Level"]
    changed = False
    while not changed:
        dis.fill(configs["Colour"]["White"])
        message("Game Level " + str(level), configs["Colour"]["Green"], configs["Colour"]["White"], configs["Display"]["Width"]//3, ((configs["Display"]["Height"] - configs["Font"]["Size"])//3 + configs["Font"]["Size"]))
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
                        change_configs()
                    changed = True

# Shoe High score
def high_score():
    show = True
    score_file_name = ("high_score_no_barrier.txt" if configs["Game"]["Type"] == 0 else "high_score_box_barrier.txt")
    while show:
        dis.fill(configs["Colour"]["White"])
        try:
            score_file = open(score_file_name, "r")
            high_score = int(score_file.read())
            score_file.close()
        except IOError:
            high_score = 0

        message("High Score : " + str(high_score), configs["Colour"]["Blue"], configs["Colour"]["White"], configs["Display"]["Width"]/3, (configs["Display"]["Height"] - configs["Font"]["Size"])/3)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER)):
                show = False

# Draw the box barrier
def draw_box():
    for i in range (configs["Display"]["Width"]//configs["Snake"]["Block"]):
        pygame.draw.rect(dis, configs["Colour"]["Red"], [(configs["Snake"]["Block"]*i), configs["Font"]["Size"] + 10, configs["Snake"]["Block"], configs["Snake"]["Block"]])
        pygame.draw.rect(dis, configs["Colour"]["Red"], [(configs["Snake"]["Block"]*i), configs["Display"]["Height"]-configs["Snake"]["Block"], configs["Snake"]["Block"], configs["Snake"]["Block"]])

    for i in range ((configs["Display"]["Height"] - (configs["Font"]["Size"] + 10))//configs["Snake"]["Block"]):
        pygame.draw.rect(dis, configs["Colour"]["Red"], [0, ((configs["Snake"]["Block"]*i) + configs["Font"]["Size"] + 10), configs["Snake"]["Block"], configs["Snake"]["Block"]])
        pygame.draw.rect(dis, configs["Colour"]["Red"], [configs["Display"]["Width"]-configs["Snake"]["Block"], ((configs["Snake"]["Block"]*i) + configs["Font"]["Size"] + 10), configs["Snake"]["Block"], configs["Snake"]["Block"]])

# Game Function
def game_loop():
    # Basic Variables
    game_close = False
    score = 0
    box_reduction = (0 if configs["Game"]["Type"] == 0 else 10)
    dis_width = configs["Display"]["Width"]
    dis_height = configs["Display"]["Height"]
    font_size = configs["Font"]["Size"]
    snake_block = configs["Snake"]["Block"]
    high_score_flag = False
    score_file_name = ("high_score_no_barrier.txt" if configs["Game"]["Type"] == 0 else "high_score_box_barrier.txt")


    # Initial state of the game
    x = int(dis_width / 2)
    y = int((dis_height - font_size) / 2) + font_size

    snake_List = []
    Length_of_snake = 1

    foodx = int(round(random.randrange(box_reduction, dis_width - snake_block - box_reduction) / 10.0) * 10)
    foody = int(round(random.randrange(font_size + box_reduction + 10, dis_height - snake_block - box_reduction) / 10.0) * 10)

    direction = [False, False, False, False]    #[Left, Up, Down, Right]

    #Game loop
    while not game_close:
        # Game Play
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_KP4) and not direction[3]:
                    direction = [True, False, False, False]
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_KP6) and not direction[0]:
                    direction = [False, False, False, True]
                elif (event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_KP8) and not direction[2]:
                    direction = [False, True, False, False]
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_KP2) and not direction[1]:
                    direction = [False, False, True, False]

        if direction[0]:
            x -= snake_block
        elif direction[1]:
            y -= snake_block
        elif direction[2]:
            y += snake_block
        elif direction[3]:
            x += snake_block

        # Barrier Logic
        if configs["Game"]["Type"] == 0:      # No Barrier
            dis.fill(configs["Colour"]["White"])
            message("No barrier", configs["Colour"]["Blue"], configs["Colour"]["White"], 10, 0)
            
            if x > dis_width - snake_block:
                x = 0
            elif x < 0:
                x = dis_width - snake_block
            if y > dis_height - snake_block:
                y = font_size + 10
            elif y < font_size + 10:
                y = dis_height - snake_block
                
        elif configs["Game"]["Type"] == 1:    # Box Barrier
            dis.fill(configs["Colour"]["White"])
            draw_box()
            message("Box barrier", configs["Colour"]["Blue"], configs["Colour"]["White"], 10, 0)
            
            if x >= (dis_width - snake_block) or x < snake_block or y >= (dis_height - snake_block) or y < (font_size + snake_block + 10):
                game_close = True
                
        message("Your Score : " + str(score), configs["Colour"]["Green"], configs["Colour"]["White"], dis_width - 200, 0)    # Display realtime score
        
        pygame.draw.rect(dis, configs["Colour"]["Green"], [foodx, foody, snake_block, snake_block])  # Food

        # Creating snake
        snake_Head = []
        snake_Head.append(x)
        snake_Head.append(y)
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Snake ate himself
        for cordinate in snake_List[:-1]:
            if cordinate == snake_Head:
                game_close = True

        draw_snake(snake_block, snake_List, configs["Colour"]["Black"])
        
        pygame.display.update()

        # Snake ate food
        if x == foodx and y == foody:
            foodx = int(round(random.randrange(box_reduction, dis_width - snake_block - box_reduction) / 10.0) * 10)
            foody = int(round(random.randrange(font_size + box_reduction + 10, dis_height - snake_block - box_reduction) / 10.0) * 10)
            Length_of_snake += 1
            score += configs["Game"]["Level"]

        clock.tick(configs["Game"]["Level"] * 5)

    # Game over
    # High Score
    dis.fill(configs["Colour"]["White"])
    try:
        score_file = open(score_file_name, "r")
        high_score = int(score_file.read())
        score_file.close()
    except IOError:
        high_score = 0
        
    if score > high_score or high_score_flag:
        message("High Score : " + str(score), configs["Colour"]["Blue"], configs["Colour"]["White"], dis_width/3, (dis_height - font_size)/3 + font_size)
        high_score = score
        high_score_flag = True
    else:
        message("Your Score : " + str(score), configs["Colour"]["Blue"], configs["Colour"]["White"], dis_width/3, (dis_height - font_size)/3 + font_size)
        high_score_flag = False

    score_file = open(score_file_name, "w")
    score_file.write(str(high_score))
    score_file.close()

    message("Game Over!", configs["Colour"]["Red"], configs["Colour"]["White"], dis_width/3, ((dis_height - font_size)/3 + 2 * font_size))
    pygame.display.update()
    time.sleep(2)

# Main Function
def main_loop():
    # Basic Variables
    game_over = False
    select_item = 0
    log_write("Init Game variables\n")

    while not game_over:
        dis.fill(configs["Colour"]["White"])
        message("Snake Game", configs["Colour"]["Green"], configs["Colour"]["White"], configs["Display"]["Width"]//3, ((configs["Display"]["Height"] - configs["Font"]["Size"])//3 + configs["Font"]["Size"]))
        item_list = ["Start Game", "Game Type", "Level", "High Score", "Quit Game"]
        for i in range(len(item_list)):
            if (select_item == i):
                f_colour = configs["Colour"]["White"]
                bg_colour = configs["Colour"]["Blue"]
            else:
                f_colour = configs["Colour"]["Blue"]
                bg_colour = configs["Colour"]["White"]
            message(item_list[i], f_colour, bg_colour, configs["Display"]["Width"]//3, ((configs["Display"]["Height"] - configs["Font"]["Size"])//3 + ((2 + i) * configs["Font"]["Size"])))
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
                        game_loop()
                    elif select_item == 1:
                        change_game_type()
                    elif select_item == 2:
                        change_game_level()
                    elif select_item == 3:
                        high_score()
                        
    log_write("Quiting the Game...\n")
    pygame.quit()
    log_write("Game Quit\n")

log_write("Define Game functions completed\n")
log_write("Starting Game...\n")

main_loop()
log_write("Game finished\nLog finished")
quit()
