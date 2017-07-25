import random

import tdl

import level
import palette

from entities import kobold
from entities import item

def generate_level(width, height):
    new_entities = []
    new_level = level.Level(0, 0, width, height)

    new_level.data.draw_str(0, 0, 'X' * width * height)

    TOP = 0b0001
    RIGHT = 0b0010
    BOTTOM = 0b0100
    LEFT = 0b1000

    map = '6CX' + \
          '3F8' + \
          'X38'

    room_templates = [
        '####.####' + \
        '#.......#' + \
        '#.......#' + \
        '.........' + \
        '#.......#' + \
        '#.......#' + \
        '####.####',
        '####.####' + \
        '#.......#' + \
        '#.......#' + \
        '#.......#' + \
        '#.......#' + \
        '#.......#' + \
        '#########',
        '#########' + \
        '#.......#' + \
        '#.......#' + \
        '#........' + \
        '#.......#' + \
        '#.......#' + \
        '#########',
        '####.####' + \
        '#.......#' + \
        '#.......#' + \
        '#........' + \
        '#.......#' + \
        '#.......#' + \
        '#########',
        '#########' + \
        '#.......#' + \
        '#.......#' + \
        '#.......#' + \
        '#.......#' + \
        '#.......#' + \
        '####.####',
        '####.####' + \
        '#.......#' + \
        '#.......#' + \
        '#.......#' + \
        '#.......#' + \
        '#.......#' + \
        '####.####',
        '#########' + \
        '#.......#' + \
        '#.......#' + \
        '#........' + \
        '#.......#' + \
        '#.......#' + \
        '####.####',
        '####.####' + \
        '#.......#' + \
        '#.......#' + \
        '#........' + \
        '#.......#' + \
        '#.......#' + \
        '####.####',
        '#########' + \
        '#.......#' + \
        '#.......#' + \
        '........#' + \
        '#.......#' + \
        '#.......#' + \
        '#########',
        '####.####' + \
        '#.......#' + \
        '#.......#' + \
        '........#' + \
        '#.......#' + \
        '#.......#' + \
        '#########',
        '#########' + \
        '#.......#' + \
        '#.......#' + \
        '.........' + \
        '#.......#' + \
        '#.......#' + \
        '#########',
        '####.####' + \
        '#.......#' + \
        '#.......#' + \
        '.........' + \
        '#.......#' + \
        '#.......#' + \
        '#########',
        '#########' + \
        '#.......#' + \
        '#.......#' + \
        '........#' + \
        '#.......#' + \
        '#.......#' + \
        '####.####',
        '####.####' + \
        '#.......#' + \
        '#.......#' + \
        '........#' + \
        '#.......#' + \
        '#.......#' + \
        '####.####',
        '#########' + \
        '#.......#' + \
        '#.......#' + \
        '.........' + \
        '#.......#' + \
        '#.......#' + \
        '####.####',
        '####.####' + \
        '#.......#' + \
        '#.......#' + \
        '.........' + \
        '#.......#' + \
        '#.......#' + \
        '####.####'
    ]

    # Build list of room Consoles
    rooms = [None for _ in range(16)]
    for i in range(16):
        con = tdl.Console(9, 7)
        con.draw_str(0, 0, room_templates[i])
        rooms[i] = con

    # Build out map
    for i, m in enumerate(map):
        x = i % 3 * 9 + 1
        y = i // 3 * 7

        if m != 'X':
            current_room = rooms[int(m, base=16)]
            new_level.data.blit(current_room, x, y)

    for (x, y) in new_level.data:
        ch, fg, bg = new_level.data.get_char(x, y)
        if ch == ord('.'):
            if random.random() < 1 / 30:
                k = kobold.Kobold(position=(x, y))
                new_entities.append(k)

            elif random.random() < 1 / 60:
                s = item.Sword(position=(x, y))
                new_entities.append(s)

            elif random.random() < 1 / 60:
                s = item.Dagger(position=(x, y))
                new_entities.append(s)

            elif random.random() < 1 / 100:
                p = item.Potion(char='!', position=(x, y), fg=palette.BRIGHT_MAGENTA)
                new_entities.append(p)

    return new_level, new_entities
