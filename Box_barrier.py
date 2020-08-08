## Created by : Sumudu Madushanka
## Last update : 8/8/2020

# Create the box barrier
def create_box(dis, dis_width, dis_height, snake_block, font_size, barrier_grid):
    for i in range (dis_width//snake_block):
        barrier_grid.append([snake_block * i, font_size + 10])
        barrier_grid.append([snake_block * i, font_size + 10 + snake_block])

        barrier_grid.append([snake_block * i, dis_height - snake_block])
        barrier_grid.append([snake_block * i, dis_height - (2 * snake_block)])

    for i in range ((dis_height - (font_size + 10))//snake_block):
        barrier_grid.append([0, ((snake_block * i) + font_size + 10)])
        barrier_grid.append([snake_block, ((snake_block * i) + font_size + 10)])

        barrier_grid.append([dis_width - snake_block, ((snake_block * i) + font_size + 10)])
        barrier_grid.append([dis_width - (2 * snake_block), ((snake_block * i) + font_size + 10)])
