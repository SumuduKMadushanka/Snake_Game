## Created by : Sumudu Madushanka
## Last update : 8/4/2020

### Game Box Barrier ###
import pygame
from time import sleep
from random import randrange
from Message import message
from Basic_game_functions import draw_snake

# Draw the box barrier
def draw_box(dis, dis_width, dis_height, snake_block, box_color, font_size):
    for i in range (dis_width//snake_block):
        pygame.draw.rect(dis, box_color, [(snake_block * i), font_size + 10, snake_block, snake_block])
        pygame.draw.rect(dis, box_color, [(snake_block * i), dis_height - snake_block, snake_block, snake_block])

    for i in range ((dis_height - (font_size + 10))//snake_block):
        pygame.draw.rect(dis, box_color, [0, ((snake_block * i) + font_size + 10), snake_block, snake_block])
        pygame.draw.rect(dis, box_color, [dis_width - snake_block, ((snake_block * i) + font_size + 10), snake_block, snake_block])

# Game Function : Box Barrier
def game_loop_box_barrier(dis, configs, clock):
    # Basic Variables
    game_close = False
    box_reduction = 10
    # Display
    dis_width = configs["Display"]["Width"]
    dis_height = configs["Display"]["Height"]
    # Colour
    lightyellow = configs["Colour"]["LightYellow"]
    red = configs["Colour"]["Red"]
    blue = configs["Colour"]["Blue"]
    green = configs["Colour"]["Green"]
    black = configs["Colour"]["Black"]
    white = configs["Colour"]["White"]
    # Font
    font_size = configs["Font"]["Size"]
    # Snake
    snake_block = configs["Snake"]["Block"]
    # Score
    score = 0
    score_unit = configs["Game"]["Level"]
    high_score_flag = False
    score_file_name = "high_score_box_barrier.txt"


    # Initial state of the game
    x = int(dis_width / 2)
    y = int((dis_height - font_size) / 2) + font_size

    snake_List = []
    Length_of_snake = 1

    foodx = int(round(randrange(box_reduction, dis_width - snake_block - box_reduction) / 10.0) * 10)
    foody = int(round(randrange(font_size + box_reduction + 10, dis_height - snake_block - box_reduction) / 10.0) * 10)

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

        bg_color = lightyellow
        dis.fill(bg_color)
        draw_box(dis, dis_width, dis_height, snake_block, red, font_size)
        message(dis, font_size, "Box barrier", blue, bg_color, 10, 0)
        
        if x >= (dis_width - snake_block) or x < snake_block or y >= (dis_height - snake_block) or y < (font_size + snake_block + 10):
            game_close = True
                
        message(dis, font_size, "Your Score : " + str(score), green, bg_color, dis_width - 200, 0)    # Display realtime score
        
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
            foodx = int(round(randrange(box_reduction, dis_width - snake_block - box_reduction) / 10.0) * 10)
            foody = int(round(randrange(font_size + box_reduction + 10, dis_height - snake_block - box_reduction) / 10.0) * 10)
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
