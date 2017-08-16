import random

import instances
import palette
import utils

from ai.actions import attackaction
from ai.actions import equipitemaction
from ai.actions import useitemaction

from entities import entity


class Item(entity.Entity):
    def get_action(self, requester=None):
        pass

    def get_special_action(self, requester, target):
        return None

    def on_use(self):
        pass


class HeldItem(Item):
    def __init__(self, char, position=(0, 0), fg=palette.BRIGHT_WHITE, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)
        self.chance_to_break = 1 / 4

    def get_action(self, requester=None):
        if requester and requester.weapon.isinstance('Fist'):
            return equipitemaction.EquipItemAction(requester, self)

        return None

    def get_perform_action(self, requester, target):
        direction = utils.math.sub(target.position, self.position)
        return attackaction.AttackAction(requester, target, direction)

    def on_use(self):
        if random.random() < self.chance_to_break:
            instances.console.print('{}\'s {} breaks!'.format(self.parent.display_string, self.display_string))

            if self.parent.isinstance('Creature'):
                self.parent.drop_weapon()

            self.remove()


class UsableItem(Item):
    def get_action(self, requester=None):
        return useitemaction.UseItemAction(requester, self)

    def use(self, target):
        instances.console.print('{} is being used on {}'.format(self.display_string, target.display_string))
