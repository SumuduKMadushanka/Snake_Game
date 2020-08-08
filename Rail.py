## Created by : Sumudu Madushanka
## Last update : 8/8/2020

# Create the Rail
def create_rail(dis, dis_width, dis_height, snake_block, font_size, barrier_grid):
    tun_width = dis_width//4
    tun_height = (dis_height - (font_size + 10))//4
    
    for i in range (dis_width//snake_block):
        barrier_grid.append([snake_block * i, font_size + 10])
        barrier_grid.append([snake_block * i, font_size + 10 + snake_block])

        barrier_grid.append([snake_block * i, dis_height - snake_block])
        barrier_grid.append([snake_block * i, dis_height - (2 * snake_block)])

    for i in range (tun_width//snake_block, (3*tun_width)//snake_block):
        barrier_grid.append([(snake_block * i), ((tun_height//snake_block) * snake_block) + font_size + 10])
        barrier_grid.append([(snake_block * i), ((tun_height//snake_block) * snake_block) + font_size + 10 + snake_block])

        barrier_grid.append([(snake_block * i), ((3 * (tun_height//snake_block)) * snake_block) + font_size + 10])    
        barrier_grid.append([(snake_block * i), ((3 * (tun_height//snake_block)) * snake_block) + font_size + 10 - snake_block])    

    for i in range (tun_height//snake_block):
        barrier_grid.append([0, ((snake_block * i) + font_size + 10)])
        barrier_grid.append([snake_block, ((snake_block * i) + font_size + 10)])

        barrier_grid.append([dis_width - snake_block, ((snake_block * i) + font_size + 10)])
        barrier_grid.append([dis_width - (2 * snake_block), ((snake_block * i) + font_size + 10)])
        
    for i in range (3*tun_height//snake_block, (dis_height - (font_size + 10))//snake_block):
        barrier_grid.append([0, ((snake_block * i) + font_size + 10)])
        barrier_grid.append([snake_block, ((snake_block * i) + font_size + 10)])

        barrier_grid.append([dis_width - snake_block, ((snake_block * i) + font_size + 10)])
        barrier_grid.append([dis_width - (2 * snake_block), ((snake_block * i) + font_size + 10)])
