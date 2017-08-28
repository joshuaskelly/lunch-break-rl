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
        self.durability = 12
        self.chance_to_break = 1 / 2

    def get_action(self, requester=None):
        if requester and requester.can_equip(self):
            return equipitemaction.EquipItemAction(requester, self)

        return None

    def get_perform_action(self, requester, target):
        direction = utils.math.sub(target.position, self.position)
        return attackaction.AttackAction(requester, target, direction)

    def on_use(self):
        self.durability -= 1

        if self.durability <= 0 and random.random() < self.chance_to_break:
            self.break_item()

    def break_item(self):
        from entities.items.weapons import debris

        old_parent = self.parent
        old_position = self.position
        self.remove()

        if old_parent.isinstance('Player'):
            old_parent.equip_weapon(debris.Debris())
            instances.console.describe(self, '{}\'s {} breaks!'.format(self.display_string, self.display_string))

        else:
            old_parent.append(debris.Debris(position=old_position))


class UsableItem(Item):
    def get_action(self, requester=None):
        return useitemaction.UseItemAction(requester, self)

    def use(self, target):
        instances.console.describe(target, '{} is being used on {}'.format(self.display_string, target.display_string))
