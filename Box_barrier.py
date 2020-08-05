## Created by : Sumudu Madushanka
## Last update : 8/5/2020

### Game Box Barrier ###
import pygame
from time import sleep
from random import randrange
from Message import message
from Basic_game_functions import draw_snake, draw_barrier, init_food, update_high_score

# Create the box barrier
def create_box(dis, dis_width, dis_height, snake_block, font_size, barrier_grid):
    for i in range (dis_width//snake_block):
        barrier_grid.append([snake_block * i, font_size + 10])
        barrier_grid.append([snake_block * i, dis_height - snake_block])

    for i in range ((dis_height - (font_size + 10))//snake_block):
        barrier_grid.append([0, ((snake_block * i) + font_size + 10)])
        barrier_grid.append([dis_width - snake_block, ((snake_block * i) + font_size + 10)])

# Game Function : Box Barrier
def game_loop_box_barrier(dis, configs, clock):
    # Basic Variables
    game_close = False
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
    barrier_grid = []
    Length_of_snake = 1

    bg_color = lightyellow
    create_box(dis, dis_width, dis_height, snake_block, font_size, barrier_grid)

    food = init_food(dis_width, dis_height, font_size, snake_block, barrier_grid)

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

        
        dis.fill(bg_color)
        draw_barrier(dis, snake_block, red, barrier_grid)
        message(dis, font_size, "Box barrier", blue, bg_color, 10, 0)
        
        if [x, y] in barrier_grid:
            game_close = True
                
        message(dis, font_size, "Your Score : " + str(score), green, bg_color, dis_width - 200, 0)    # Display realtime score
        
        pygame.draw.rect(dis, green, [food[0], food[1], snake_block, snake_block])  # Food

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
        if x == food[0] and y == food[1]:
            food = init_food(dis_width, dis_height, font_size, snake_block, barrier_grid)
            Length_of_snake += 1
            score += score_unit

        clock.tick(score_unit * 5)

    # Game over
    sleep(2)
    # High Score
    dis.fill(white)
    update_high_score(dis, dis_width, dis_height, score_file_name, score, font_size, blue, white)

    message(dis, font_size, "Game Over!", red, white, dis_width/3, ((dis_height - font_size)/3 + 2 * font_size))
    pygame.display.update()
    sleep(2)
