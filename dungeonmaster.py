import random

import palette
import scene

from ai import action
from entities import creature
from entities import kobold
from entities import item

class DungeonMaster(object):
    def __init__(self):
        self.name = 'Jim'

    def draw(self, console):
        pass

    def update(self, time):
        pass

    def tick(self):
        roll = random.random()

        if roll <= 0.125:
            roll = random.random()
            current_scene = scene.Scene.current_scene
            level = current_scene.level
            position = random.randint(1, level.width - 1) + level.x, random.randint(1, level.height + level.y - 1)

            if roll <= 0.2:
                k = kobold.Kobold(position=position)
                current_scene.entities.append(k)

            elif roll <= 0.3:
                s = item.Sword(position=position, fg=palette.BRIGHT_YELLOW)
                current_scene.entities.append(s)

            elif roll <= 0.4:
                p = item.Potion(char='!', position=position, fg=palette.BRIGHT_MAGENTA)
                p.name = 'potion'
                current_scene.entities.append(p)

    def handle_events(self, event):
        if event.type == 'TICK':
            self.tick()
