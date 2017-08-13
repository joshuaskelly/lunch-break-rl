import random

import instances
import utils

from ai import action
from entities import entity
from entities import creature


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
        if other.held_item.__class__.__name__ == 'Fist':
            return action.EquipItemAction(self)

        return None

    def get_perform_action(self, target):
        direction = utils.math.sub(target.position, self.position)
        return action.AttackAction(direction)

    def on_use(self):
        if random.random() < self.chance_to_break:
            instances.console.print('{} {} breaks!'.format(self.parent.name, self.name))

            if isinstance(self.parent, creature.Creature):
                self.parent.drop_held_item()

            self.remove()


class UsableItem(Item):
    def get_action(self, other=None):
        return action.UseItemAction(self)

    def use(self, target):
        instances.console.print('{} is being used on {}'.format(self.name, target.name))
