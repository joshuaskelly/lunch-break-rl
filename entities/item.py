import random

import instances
import utils

from ai.actions import attackaction
from ai.actions import equipitemaction
from ai.actions import useitemaction

from entities import entity


class Item(entity.Entity):
    def get_action(self, other=None):
        pass

    def get_special_action(self, target):
        return None

    def on_use(self):
        pass


class HeldItem(Item):
    def __init__(self, char, position=(0, 0), fg=(255, 255, 255),  bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)
        self.chance_to_break = 1 / 4

    def get_action(self, other=None):
        if other.held_item.isinstance('Fist'):
            return equipitemaction.EquipItemAction(self)

        return None

    def get_perform_action(self, target):
        direction = utils.math.sub(target.position, self.position)
        return attackaction.AttackAction(direction)

    def on_use(self):
        if random.random() < self.chance_to_break:
            instances.console.print('{} {} breaks!'.format(self.parent.name, self.name))

            if self.parent.isinstance('Creature'):
                self.parent.drop_held_item()

            self.remove()


class UsableItem(Item):
    def get_action(self, other=None):
        return useitemaction.UseItemAction(self)

    def use(self, target):
        instances.console.print('{} is being used on {}'.format(self.name, target.name))
