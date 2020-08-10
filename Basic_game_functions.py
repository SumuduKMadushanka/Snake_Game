## Created by : Sumudu Madushanka
## Last update : 8/10/2020

import pygame
import json
from time import sleep
from random import randrange
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
        message(dis, (2 * configs["Font"]["Size"]), "Game Type", configs["Colour"]["Green"], configs["Colour"]["White"], configs["Display"]["Width"]/4, (configs["Display"]["Height"] - configs["Font"]["Size"])/4)
        item_list = ["No Barrier", "Box Barrier", "Tunnel", "Rail", "Mill"]
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
        message(dis, (2 * configs["Font"]["Size"]), "Game Level", configs["Colour"]["Green"], configs["Colour"]["White"], configs["Display"]["Width"]//4, (configs["Display"]["Height"] - configs["Font"]["Size"])//4)
        message(dis, configs["Font"]["Size"], "Level: " + str(level), configs["Colour"]["Blue"], configs["Colour"]["White"], configs["Display"]["Width"]//3, ((configs["Display"]["Height"] - configs["Font"]["Size"])//3 + configs["Font"]["Size"]))
        pygame.draw.rect(dis, configs["Colour"]["Blue"], [configs["Display"]["Width"]//3, ((configs["Display"]["Height"] - configs["Font"]["Size"])//3 + (2 * configs["Font"]["Size"])), 25 * level, 20])

        if level < 5:
            pygame.draw.rect(dis, configs["Colour"]["LightBlue"], [configs["Display"]["Width"]//3 + (25 * level), ((configs["Display"]["Height"] - configs["Font"]["Size"])//3 + (2 * configs["Font"]["Size"])), (25 * (5 - level)), 20])

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
def high_score(dis, game_type, bg_colour, title_coolour, font_colour, font_size, dis_width, dis_height):
    show = True
    game_type_list = ["No Barrier", "Box Barrier", "Tunnel", "Rail", "Mill"]
    score_file_name = "high_score.json"

    try:
        high_score_file = open(score_file_name, "r")
        high_score_dict = json.load(high_score_file)
        high_score_file.close()

        high_score_list = high_score_dict[game_type_list[game_type]]
        
    except FileNotFoundError:
        high_score_dict = {}
        for g_type in game_type_list:
            high_score_dict[g_type] = [0 for i in range(5)]
        
        high_score_file = open(score_file_name, "w")
        json.dump(high_score_dict, high_score_file, indent = 4)
        high_score_file.close()

        high_score_list = high_score_dict[game_type_list[game_type]]

    except KeyError:
        high_score_file = open(score_file_name, "r")
        high_score_dict = json.load(high_score_file)
        high_score_file.close()

        high_score_dict[game_type_list[game_type]] = [0 for i in range(5)]
        high_score_file = open(score_file_name, "w")
        json.dump(high_score_dict, high_score_file, indent = 4)
        high_score_file.close()

        high_score_list = high_score_dict[game_type_list[game_type]]
        
    while show:
        dis.fill(bg_colour)

        message(dis, (2 * font_size), "High Score", title_coolour, bg_colour, dis_width/4, (dis_height - font_size)/4)
        message(dis, font_size, game_type_list[game_type], title_coolour, bg_colour, dis_width/3, (dis_height - font_size)/3 + font_size)
        
        for i in range(5):
            message(dis, font_size, str(i + 1) + ") " + str(high_score_list[i]), font_colour, bg_colour, dis_width/3, (dis_height - font_size)/3 + ((2 + i) * font_size))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER)):
                show = False

# Update High Score
def update_high_score(dis, dis_width, dis_height, score, game_type, font_size, font_colour, bg_colour):
    game_type_list = ["No Barrier", "Box Barrier", "Tunnel", "Rail", "Mill"]
    score_file_name = "high_score.json"
    try:
        high_score_file = open(score_file_name, "r")
        high_score_dict = json.load(high_score_file)
        high_score_file.close()

        high_score_list = high_score_dict[game_type_list[game_type]]

    except FileNotFoundError:
        high_score_dict = {}
        for g_type in game_type_list:
            high_score_dict[g_type] = [0 for i in range(5)]
        
        high_score_file = open(score_file_name, "w")
        json.dump(high_score_dict, high_score_file, indent = 4)
        high_score_file.close()

        high_score_list = high_score_dict[game_type_list[game_type]]

    except KeyError:
        high_score_file = open(score_file_name, "r")
        high_score_dict = json.load(high_score_file)
        high_score_file.close()

        high_score_dict[game_type_list[game_type]] = [0 for i in range(5)]
        high_score_file = open(score_file_name, "w")
        json.dump(high_score_dict, high_score_file, indent = 4)
        high_score_file.close()

        high_score_list = high_score_dict[game_type_list[game_type]]

    place = 6
    for i in range(5):
        if score > high_score_list[i]:
            high_score_list = high_score_list[:i] + [score] + high_score_list[i:4]
            high_score_dict[game_type_list[game_type]] = high_score_list
            place = i + 1
            break

    if place == 1:
        message(dis, font_size, "Snake Master", font_colour, bg_colour, dis_width/3, (dis_height - font_size)/3 + font_size)
    elif place < 6:
        message(dis, font_size, "High Score", font_colour, bg_colour, dis_width/3, (dis_height - font_size)/3 + font_size)
    else:
        message(dis, font_size, "Your Score", font_colour, bg_colour, dis_width/3, (dis_height - font_size)/3 + font_size)

    message(dis, font_size, str(score), font_colour, bg_colour, dis_width/3, (dis_height - font_size)/3 + (2 * font_size))

    high_score_file = open(score_file_name, "w")
    json.dump(high_score_dict, high_score_file, indent = 4)
    high_score_file.close()

# Draw the snake
def draw_snake(dis, snake_block, snake_list, Snake_colour):
    for cordinate in snake_list:
        pygame.draw.rect(dis, Snake_colour, [cordinate[0], cordinate[1], snake_block, snake_block])
        
# Draw the barrier
def draw_barrier(dis, snake_block, colour, barrier_grid):
    for cordinate in barrier_grid:
        pygame.draw.rect(dis, colour, [cordinate[0], cordinate[1], snake_block, snake_block])

# Init Food No Barrier
def init_food_no_barrier(dis_width, dis_height, font_size, snake_block):
    food = []
    foodx = round(randrange(0, dis_width - snake_block) // 10.0) * 10
    foody = round(randrange(font_size + 10, dis_height - snake_block) // 10.0) * 10
    food.append(foodx)
    food.append(foody)
    return food

# Init Food
def init_food(dis_width, dis_height, font_size, snake_block, barrier_grid):
    food = init_food_no_barrier(dis_width, dis_height, font_size, snake_block)
    while (food in barrier_grid):
        food = init_food_no_barrier(dis_width, dis_height, font_size, snake_block)
    return food

# Game Function No Barrier
def game_loop_no_barrier(dis, configs, clock):
    # Basic Variables
    game_close = False
    game_over_time = 2
    # Display
    dis_width = configs["Display"]["Width"]
    dis_height = configs["Display"]["Height"]
    # Game Colours
    snake_colour = configs["Colour"][configs["Game"]["Colour_Code"][0]["Snake"]]
    food_colour = configs["Colour"][configs["Game"]["Colour_Code"][0]["Food"]]
    type_colour = configs["Colour"][configs["Game"]["Colour_Code"][0]["Type"]]
    score_colour = configs["Colour"][configs["Game"]["Colour_Code"][0]["Score"]]
    bg_colour = configs["Colour"][configs["Game"]["Colour_Code"][0]["Background"]]
    # Font
    font_size = configs["Font"]["Size"]
    font_colour = configs["Colour"]["Blue"]
    font_bg_colour = configs["Colour"]["White"]
    game_over_colour = configs["Colour"]["Red"]
    # Snake
    snake_block = configs["Snake"]["Block"]
    # Score
    score = 0
    score_unit = configs["Game"]["Level"]

    # Initial state of the game
    x = int(dis_width // 2)
    y = int((dis_height - font_size) // 2) + font_size

    snake_List = []
    Length_of_snake = 1

    food = init_food_no_barrier(dis_width, dis_height, font_size, snake_block)
    
    direction = [False, False, False, False]    #[Left, Up, Down, Right]

    #Game loop
    while not game_close:
        # Game Play
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
                game_over_time = 0
                break
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_KP4) and not direction[3]:
                    direction = [True, False, False, False]
                    break
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_KP6) and not direction[0]:
                    direction = [False, False, False, True]
                    break
                elif (event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_KP8) and not direction[2]:
                    direction = [False, True, False, False]
                    break
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_KP2) and not direction[1]:
                    direction = [False, False, True, False]
                    break

        pygame.event.clear()

        if direction[0]:
            x -= snake_block
        elif direction[1]:
            y -= snake_block
        elif direction[2]:
            y += snake_block
        elif direction[3]:
            x += snake_block

        dis.fill(bg_colour)
        message(dis, font_size, "No barrier", type_colour, bg_colour, 10, 0)
        
        if x > dis_width - snake_block:
            x = 0
        elif x < 0:
            x = dis_width - snake_block
        if y > dis_height - snake_block:
            y = font_size + 10
        elif y < font_size + 10:
            y = dis_height - snake_block
                
        message(dis, font_size, "Your Score : " + str(score), score_colour, bg_colour, dis_width - 200, 0)     # Display realtime score

        pygame.draw.rect(dis, type_colour, [0, font_size + 5, dis_width, 5])
        
        pygame.draw.rect(dis, food_colour, [food[0], food[1], snake_block, snake_block])  # Food

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

        draw_snake(dis, snake_block, snake_List, snake_colour)
        
        pygame.display.update()

        # Snake ate food
        if x == food[0] and y == food[1]:
            food = init_food_no_barrier(dis_width, dis_height, font_size, snake_block)
            Length_of_snake += 1
            score += score_unit

        clock.tick(score_unit * 5)

    # Game over
    sleep(game_over_time)
    # High Score
    dis.fill(font_bg_colour)
    update_high_score(dis, dis_width, dis_height, score, 0, font_size, font_colour, font_bg_colour)

    message(dis, font_size, "Game Over!", game_over_colour, font_bg_colour, dis_width/3, ((dis_height - font_size)/3 + 3 * font_size))
    pygame.display.update()
    sleep(2)
    pygame.event.clear()

# Game Function
def game_loop(dis, configs, clock):
    # Basic Variables
    game_close = False
    game_over_time = 2
    game_type = ""
    # Display
    dis_width = configs["Display"]["Width"]
    dis_height = configs["Display"]["Height"]
    # Game Colours
    snake_colour = configs["Colour"][configs["Game"]["Colour_Code"][configs["Game"]["Type"]]["Snake"]]
    food_colour = configs["Colour"][configs["Game"]["Colour_Code"][configs["Game"]["Type"]]["Food"]]
    type_colour = configs["Colour"][configs["Game"]["Colour_Code"][configs["Game"]["Type"]]["Type"]]
    score_colour = configs["Colour"][configs["Game"]["Colour_Code"][configs["Game"]["Type"]]["Score"]]
    bg_colour = configs["Colour"][configs["Game"]["Colour_Code"][configs["Game"]["Type"]]["Background"]]
    barrier_colour = configs["Colour"][configs["Game"]["Colour_Code"][configs["Game"]["Type"]]["Barrier"]]
    # Font
    font_size = configs["Font"]["Size"]
    font_colour = configs["Colour"]["Blue"]
    font_bg_colour = configs["Colour"]["White"]
    game_over_colour = configs["Colour"]["Red"]
    # Snake
    snake_block = configs["Snake"]["Block"]
    # Score
    score = 0
    score_unit = configs["Game"]["Level"]
    
    # Initial state of the game
    x = int(dis_width // 2)
    y = int((dis_height - font_size) // 2) + font_size

    snake_List = []
    barrier_grid = []
    Length_of_snake = 1

    if configs["Game"]["Type"] == 1:
        game_type = "Box Barrier"
        from Box_barrier import create_box
        create_box(dis, dis_width, dis_height, snake_block, font_size, barrier_grid)

    elif configs["Game"]["Type"] == 2:
        game_type = "Tunnel"
        from Tunnel import create_tunnel
        create_tunnel(dis, dis_width, dis_height, snake_block, font_size, barrier_grid)

    elif configs["Game"]["Type"] == 3:
        game_type = "Rail"
        from Rail import create_rail
        create_rail(dis, dis_width, dis_height, snake_block, font_size, barrier_grid)

    elif configs["Game"]["Type"] == 4:
        game_type = "Mill"
        from Mill import create_mill
        create_mill(dis, dis_width, dis_height, snake_block, font_size, barrier_grid)
    
    food = init_food(dis_width, dis_height, font_size, snake_block, barrier_grid)
    
    direction = [False, False, False, False]    # [Left, Up, Down, Right]

    # Game loop
    while not game_close:
        # Game Play
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
                game_over_time = 0
                break
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_KP4) and not direction[3]:
                    direction = [True, False, False, False]
                    break
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_KP6) and not direction[0]:
                    direction = [False, False, False, True]
                    break
                elif (event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_KP8) and not direction[2]:
                    direction = [False, True, False, False]
                    break
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_KP2) and not direction[1]:
                    direction = [False, False, True, False]
                    break

        pygame.event.clear()

        if direction[0]:
            x -= snake_block
        elif direction[1]:
            y -= snake_block
        elif direction[2]:
            y += snake_block
        elif direction[3]:
            x += snake_block

        dis.fill(bg_colour)
        draw_barrier(dis, snake_block, barrier_colour, barrier_grid)
        message(dis, font_size, game_type, type_colour, bg_colour, 10, 0)

        if [x, y] in barrier_grid:
            game_close = True
        elif x > dis_width - snake_block:
            x = 0
        elif x < 0:
            x = dis_width - snake_block
        if y > dis_height - snake_block:
            y = font_size + 10
        elif y < font_size + 10:
            y = dis_height - snake_block
        
        if [x, y] in barrier_grid:
            game_close = True
                
        message(dis, font_size, "Your Score : " + str(score), score_colour, bg_colour, dis_width - 200, 0)    # Display realtime score
        
        pygame.draw.rect(dis, type_colour, [0, font_size + 5, dis_width, 5])

        pygame.draw.rect(dis, food_colour, [food[0], food[1], snake_block, snake_block])  # Food

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

        draw_snake(dis, snake_block, snake_List, snake_colour)
        
        pygame.display.update()

        # Snake ate food
        if x == food[0] and y == food[1]:
            food = init_food(dis_width, dis_height, font_size, snake_block, barrier_grid)
            Length_of_snake += 1
            score += score_unit

        clock.tick(score_unit * 5)

    # Game over
    sleep(game_over_time)
    # High Score
    dis.fill(font_bg_colour)
    update_high_score(dis, dis_width, dis_height, score, configs["Game"]["Type"], font_size, font_colour, font_bg_colour)

    message(dis, font_size, "Game Over!", game_over_colour, font_bg_colour, dis_width/3, ((dis_height - font_size)/3 + 2 * font_size))
    pygame.display.update()
    sleep(2)
    pygame.event.clear()