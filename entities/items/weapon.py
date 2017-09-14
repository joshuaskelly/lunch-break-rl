import random

import palette
import utils

from ai.actions import attackaction
from entities import item


class Weapon(item.HeldItem):
    def __init__(self, char='w', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)
        self.state = WeaponState(self)
        self.damage = 3
        self.range = 1
        self.verb = 'hits'

    def in_range(self, target):
        if not target:
            return False

        distance = utils.math.distance(self.parent.position, target.position)
        return distance <= self.range

    def tick(self, tick):
        super().tick(tick)

        if self.parent.isinstance('Creature'):
            self.state.tick(tick)

    @property
    def Action(self):
        return attackaction.AttackAction


class WeaponState(attackaction.AttackActionInterface):
    def __init__(self, weapon):
        self.weapon = weapon

    def tick(self, tick):
        pass

    def can_attack(self, other):
        return self.weapon.parent and self.weapon.parent.alive and self.weapon.in_range(other)

    def allow_attack(self, action):
        return True

    def before_attacked(self, action):
        pass

    def on_attacked(self, action):
        pass

    def after_attacked(self, action):
        pass

    def before_attack(self, action):
        pass

    def after_attack(self, action):
        self.weapon.on_use()
