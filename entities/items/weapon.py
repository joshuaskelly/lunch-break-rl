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
        self.name = 'weapon'
        self.verb = 'hits'

    def in_range(self, target):
        if not target:
            return False

        distance = utils.math.distance(self.parent.position, target.position)
        return distance <= self.range

    @property
    def Action(self):
        return attackaction.AttackAction


class WeaponState(attackaction.AttackActionInterface):
    def __init__(self, weapon):
        self.weapon = weapon

    def can_attack(self, other):
        return self.weapon.in_range(other)

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
        pass