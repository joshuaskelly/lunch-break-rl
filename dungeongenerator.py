import random

import tdl

import level
import palette
import utils

from data import room_templates
from entities import entity
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
    MASK = 0b1111
    STAIRDOWN = 0b010000
    STAIRUP = 0b100000

    floor = [0x0,0x0,0x0,
             0x0,0x0,0x0,
             0x0,0x0,0x0]

    cursor = random.randint(0, 2)
    floor[cursor] |= STAIRUP

    def up():
        nonlocal floor
        nonlocal cursor
        if cursor >= 3:
            floor[cursor] |= TOP
            cursor -= 3
            floor[cursor] |= BOTTOM

            return cursor

        return None

    def down():
        nonlocal floor
        nonlocal cursor
        if cursor <= 5:
            floor[cursor] |= BOTTOM
            cursor += 3
            floor[cursor] |= TOP
            return cursor

        return None

    def right():
        nonlocal floor
        nonlocal cursor
        if cursor not in [2, 5, 8]:
            floor[cursor] |= RIGHT
            cursor += 1
            floor[cursor] |= LEFT
            return cursor
        return None

    def left():
        nonlocal floor
        nonlocal cursor
        if cursor not in [0, 3, 6]:
            floor[cursor] |= LEFT
            cursor -= 1
            floor[cursor] |= RIGHT
            return cursor
        return None

    possible_moves = [up, down, left, right]

    moves = random.randint(8, 20)
    while moves > 0:
        current_cursor = possible_moves[random.randint(0,3)]()
        if current_cursor:
            moves -= 1

    floor[cursor] |= STAIRDOWN

    # Build out floor
    for i, m in enumerate(floor):
        x = i % 3 * 9 + 1
        y = i // 3 * 7

        current_room = tdl.Console(9, 7)
        templates = room_templates[m & MASK]
        room = templates[random.randint(0, len(templates) - 1)]
        current_room.draw_str(0, 0, room)

        new_level.data.blit(current_room, x, y)

        if m & STAIRUP:
            rect = utils.rect(x, y, 9, 7)
            potential_coords = []
            for point in rect:
                ch, fg, bg = new_level.data.get_char(*point)
                if ch == ord('.'):
                    potential_coords.append(point)

            coord = potential_coords[random.randint(0, len(potential_coords) - 1)]

            ent = entity.Entity('<', coord, fg=palette.BRIGHT_YELLOW)
            ent.name = "Stairs Up"
            new_entities.append(ent)


        if m & STAIRDOWN:
            rect = utils.rect(x, y, 9, 7)
            potential_coords = []
            for point in rect:
                ch, fg, bg = new_level.data.get_char(*point)
                if ch == ord('.'):
                    potential_coords.append(point)

            coord = potential_coords[random.randint(0, len(potential_coords) - 1)]

            ent = entity.Entity('>', coord, fg=palette.BRIGHT_YELLOW)
            ent.name = "Stairs Down"
            new_entities.append(ent)

    # Placing Entities
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
