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

        if roll <= 0.1:
            roll = random.random()
            current_scene = scene.Scene.current_scene
            level = current_scene.level

            position = random.randint(1, level.width - 1) + level.x, random.randint(1, level.height + level.y - 1)
            tries = 0

            while not scene.Scene.current_scene.check_collision(*position) and tries < 10:
                position = random.randint(1, level.width - 1) + level.x, random.randint(1, level.height + level.y - 1)
                tries += 1

            if tries == 10:
                return

            if roll <= 0.4:
                k = kobold.Kobold(position=position)
                current_scene.entities.append(k)

            elif roll <= 0.5:
                s = item.Sword(position=position)
                current_scene.entities.append(s)

            elif roll <= 0.6:
                p = item.Potion(char='!', position=position, fg=palette.BRIGHT_MAGENTA)
                p.name = 'potion'
                current_scene.entities.append(p)

            elif roll <= 0.7:
                d = item.Dagger(position=position)
                current_scene.entities.append(d)

    def handle_events(self, event):
        if event.type == 'TICK':
            self.tick()
