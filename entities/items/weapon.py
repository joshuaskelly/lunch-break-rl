import palette
import utils

from ai.actions import attackaction
from entities import item


class Weapon(item.HeldItem):
    def __init__(self, char='w', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
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

    def on_attack(self, action):
        print('{} {} {} for {} damage!'.format(action.performer.name,
                                               action.performer.weapon.verb,
                                               action.target.name,
                                               action.performer.weapon.damage))

    def after_attack(self, action):
        pass