## Created by : Sumudu Madushanka
## Last update : 8/4/2020

### Game No Barrier ###
import pygame
from time import sleep
from random import randrange
from Message import message
from Basic_game_functions import draw_snake

# Game Function : No Barrier
def game_loop_no_barrier(dis, configs, clock):
    # Basic Variables
    game_close = False
    # Display
    dis_width = configs["Display"]["Width"]
    dis_height = configs["Display"]["Height"]
    # Colour
    white = configs["Colour"]["White"]
    blue = configs["Colour"]["Blue"]
    green = configs["Colour"]["Green"]
    black = configs["Colour"]["Black"]
    red = configs["Colour"]["Red"]
    # Font
    font_size = configs["Font"]["Size"]
    # Snake
    snake_block = configs["Snake"]["Block"]
    # Score
    score = 0
    score_unit = configs["Game"]["Level"]
    high_score_flag = False
    score_file_name = "high_score_no_barrier.txt"

    # Initial state of the game
    x = int(dis_width / 2)
    y = int((dis_height - font_size) / 2) + font_size

    snake_List = []
    Length_of_snake = 1

    foodx = int(round(randrange(0, dis_width - snake_block) / 10.0) * 10)
    foody = int(round(randrange(font_size + 10, dis_height - snake_block) / 10.0) * 10)

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
        bg_color = white
        dis.fill(bg_color)
        message(dis, font_size, "No barrier", blue, bg_color, 10, 0)
        
        if x > dis_width - snake_block:
            x = 0
        elif x < 0:
            x = dis_width - snake_block
        if y > dis_height - snake_block:
            y = font_size + 10
        elif y < font_size + 10:
            y = dis_height - snake_block
                
        message(dis, font_size, "Your Score : " + str(score), green, bg_color, dis_width - 200, 0)     # Display realtime score
        
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])  # Food

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

        draw_snake(dis, snake_block, snake_List, black)
        
        pygame.display.update()

        # Snake ate food
        if x == foodx and y == foody:
            foodx = int(round(randrange(0, dis_width - snake_block) / 10.0) * 10)
            foody = int(round(randrange(font_size + 10, dis_height - snake_block) / 10.0) * 10)
            Length_of_snake += 1
            score += score_unit

        clock.tick(score_unit * 5)

    # Game over
    # High Score
    dis.fill(white)
    try:
        score_file = open(score_file_name, "r")
        high_score = int(score_file.read())
        score_file.close()
    except IOError:
        high_score = 0
        
    if score > high_score or high_score_flag:
        message(dis, font_size, "High Score : " + str(score), blue, white, dis_width/3, (dis_height - font_size)/3 + font_size)
        high_score = score
        high_score_flag = True
    else:
        message(dis, font_size, "Your Score : " + str(score), blue, white, dis_width/3, (dis_height - font_size)/3 + font_size)
        high_score_flag = False

    score_file = open(score_file_name, "w")
    score_file.write(str(high_score))
    score_file.close()

    message(dis, font_size, "Game Over!", red, white, dis_width/3, ((dis_height - font_size)/3 + 2 * font_size))
    pygame.display.update()
    sleep(2)
