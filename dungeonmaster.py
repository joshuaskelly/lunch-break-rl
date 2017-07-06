import random

import palette
import scene

from ai import action
from entities import creature
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

        if roll <= 0.5:
            roll = random.random()
            current_scene = scene.Scene.current_scene
            level = current_scene.level
            position = random.randint(0, level.width) + level.x, random.randint(0, level.height + level.y)

            if roll <= 0.2:
                npc = creature.Creature(char='K', position=position, fg=palette.BRIGHT_RED)
                npc.name = 'kobold'
                npc.brain.add_action(action.IdleAction())
                current_scene.entities.append(npc)

            elif roll <= 0.3:
                s = item.Sword(position=position, fg=palette.BRIGHT_YELLOW)
                s.name = 'sword'
                current_scene.entities.append(s)

            elif roll <= 0.4:
                p = item.Potion(char='!', position=position, fg=palette.BRIGHT_MAGENTA)
                p.name = 'potion'
                current_scene.entities.append(p)

    def handle_events(self, event):
        if event.type == 'TICK':
            self.tick()
