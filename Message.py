## Created by : Sumudu Madushanka
## Last update : 8/4/2020

from pygame import font

### Message Functions ###
# Write a message on screen
def message(dis, font_size, msg, colour, bg_colour, x, y):
    font_style = font.SysFont(None, font_size)
    mesg = font_style.render(msg, True, colour, bg_colour)
    dis.blit(mesg, [int(x), int(y)])
