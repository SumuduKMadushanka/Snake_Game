## Created by : Sumudu Madushanka
## Last update : 8/8/2020

# Create the Mill
def create_mill(dis, dis_width, dis_height, snake_block, font_size, barrier_grid):
    width = dis_width//3
    height = (dis_height - (font_size + 10))//3

    for i in range ((2 * height)//snake_block):
        barrier_grid.append([width, ((snake_block * i) + font_size + 10)])
        barrier_grid.append([width + snake_block, ((snake_block * i) + font_size + 10)])

    for i in range (height//snake_block, (dis_height - (font_size + 10))//snake_block):
        barrier_grid.append([(2 * width), ((snake_block * i) + font_size + 10)])
        barrier_grid.append([(2 * width) - snake_block, ((snake_block * i) + font_size + 10)])

    for i in range ((width + (2 * snake_block))//snake_block):
        barrier_grid.append([(snake_block * i), ((((2 * height) + (height//2))//snake_block)*snake_block) + font_size + 10])
        barrier_grid.append([(snake_block * i), ((((2 * height) + (height//2))//snake_block)*snake_block) + font_size + 10 + snake_block])

    for i in range (((2 * width) - snake_block)//snake_block, dis_width//snake_block):
        barrier_grid.append([(snake_block * i), (((height//2)//snake_block)*snake_block) + font_size + 10])
        barrier_grid.append([(snake_block * i), (((height//2)//snake_block)*snake_block) + font_size + 10 - snake_block])