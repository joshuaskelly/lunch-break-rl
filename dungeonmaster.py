import random

import palette
from entities import item
from entities import kobold
from scenes import gamescene


class DungeonMaster(object):
    def __init__(self):
        self.name = 'Jim'

    def draw(self, console):
        pass

    def update(self, time):
        pass

    def tick(self, tick_number):
        roll = random.random()

        if roll <= 0.15:
            roll = random.random()
            current_scene = gamescene.GameScene.current_scene.level_scene
            level = current_scene.level

            position = random.randint(1, level.width - 1) + level.x, random.randint(1, level.height + level.y - 1)
            tries = 0

            while not gamescene.GameScene.current_scene.level_scene.check_collision(*position) and tries < 10:
                position = random.randint(1, level.width - 1) + level.x, random.randint(1, level.height + level.y - 1)
                tries += 1

            if tries == 10:
                return

            if roll <= 0.6:
                k = kobold.Kobold(position=position)
                current_scene.entities.append(k)

            elif roll <= 0.7:
                s = item.Sword(position=position)
                current_scene.entities.append(s)

            elif roll <= 0.8:
                p = item.Potion(char='!', position=position, fg=palette.BRIGHT_MAGENTA)
                p.name = 'potion'
                current_scene.entities.append(p)

            elif roll <= 0.9:
                d = item.Dagger(position=position)
                current_scene.entities.append(d)

            elif roll <= 1:
                d = item.Glove(position=position)
                current_scene.entities.append(d)
