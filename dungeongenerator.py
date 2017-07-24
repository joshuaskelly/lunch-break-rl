import tdl

import level

def generate_level(width, height):
    new_level = level.Level(0, 0, width, height)

    r = tdl.Console(9, 7)
    r.draw_str(0, 0, '##########.......##.......##.......##.......##.......##########')

    for x in [1, 10, 19]:
        for y in [0, 7, 14]:
            new_level.data.blit(r, x, y)

    return new_level