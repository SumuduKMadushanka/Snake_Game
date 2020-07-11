## Created by : Sumudu Madushanka
## Last update : 11/7/2020

import pygame
import time
import random
 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

font_size = 30
 
dis_width = 600
dis_height = 400 + font_size
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('pygame test')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15
score_factor = 1
 
font_style = pygame.font.SysFont(None, font_size)

def draw_snake(snake_block, snake_list):
    for cordinate in snake_list:
        pygame.draw.rect(dis, black, [cordinate[0], cordinate[1], snake_block, snake_block])
 
def message(msg, color, x, y):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [int(x), int(y)])
 
 
def gameLoop():  # creating a function
    game_over = False
    game_close = False
    game_type = -1
    score = 0
    high_score_flag = False
    score_file_name = ""
    
    while True:
        dis.fill(white)
        message("Select Game Type", blue, dis_width/3, ((dis_height - font_size)/3 + font_size))
        message("1 - No barrier", blue, dis_width/3, (dis_height - font_size)/3 + (2 * font_size))
        message("2 - Box Barrier", blue, dis_width/3, (dis_height - font_size)/3 + (3 * font_size))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_type = 1
                    score_file_name = "high_score_no_barrier.txt"
                if event.key == pygame.K_2:
                    game_type = 2
                    score_file_name = "high_score_box_barrier.txt"
        if game_type != -1 or game_over != False:
            break
        
 
    x = int(dis_width / 2)
    y = int((dis_height - font_size) / 2) + font_size
 
    x_change = 0
    y_change = 0

    snake_List = []
    Length_of_snake = 1
 
    foodx = int(round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0)
    foody = int(round(random.randrange(font_size + 10, dis_height - snake_block) / 10.0) * 10.0)

    prev_key = pygame.K_0
    while not game_over:
        while game_close == True and game_over == False:
            dis.fill(white)
            try:
                score_file = open(score_file_name, "r")
                high_score = int(score_file.read())
                score_file.close()
            except IOError:
                high_score = 0
                
            if score > high_score or high_score_flag:
                message("High Score : " + str(score), blue, dis_width/3, (dis_height - font_size)/3 + font_size)
                high_score = score
                high_score_flag = True
            else:
                message("Your Score : " + str(score), blue, dis_width/3, (dis_height - font_size)/3 + font_size)
                
            message("Press Q-Quit or C-Play Again", red, dis_width/3, (dis_height - font_size)/3 + (2 * font_size))
            pygame.display.update()

            score_file = open(score_file_name, "w")
            score_file.write(str(high_score))
            score_file.close()
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and prev_key != pygame.K_RIGHT:
                    x_change = -snake_block
                    y_change = 0
                    prev_key = event.key
                elif event.key == pygame.K_RIGHT and prev_key != pygame.K_LEFT:
                    x_change = snake_block
                    y_change = 0
                    prev_key = event.key
                elif event.key == pygame.K_UP and prev_key != pygame.K_DOWN:
                    y_change = -snake_block
                    x_change = 0
                    prev_key = event.key
                elif event.key == pygame.K_DOWN and prev_key != pygame.K_UP:
                    y_change = snake_block
                    x_change = 0
                    prev_key = event.key

        if game_type == 1:
            score_factor = 5
            dis.fill(white)
            message("No barrier", blue, 10, 0)
            if x > dis_width:
                x = 0
            elif x < 0:
                x = dis_width
            if y > dis_height:
                y = font_size + 10
            elif y < font_size + 10:
                y = dis_height
                
        elif game_type == 2:
            score_factor = 3
            dis.fill(yellow)
            message("Box barrier", blue, 0, 0)
            if x >= dis_width or x < 0 or y >= dis_height or y < font_size + 10:
                game_close = True

        message("Your Score : " + str(score), green, dis_width - 200, 0)
 
        x += x_change
        y += y_change
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x)
        snake_Head.append(y)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for cordinate in snake_List[:-1]:
            if cordinate == snake_Head:
                game_close = True

        draw_snake(snake_block, snake_List)
        
        pygame.display.update()
 
        if x == foodx and y == foody:
            foodx = int(round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0)
            foody = int(round(random.randrange(font_size + 10, dis_height - snake_block) / 10.0) * 10.0)
            Length_of_snake += 1
            score += int(snake_speed / score_factor)
        clock.tick(snake_speed)

    dis.fill(white)
    message("Game Over!", red, dis_width/3, ((dis_height - font_size)/3 + font_size))
    pygame.display.update()
    time.sleep(1)
    pygame.quit()
    quit()
 
 
gameLoop()
