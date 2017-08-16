import random

import instances
import palette
import registry

from entities import animation
from entities.items import weapon


class Sword(weapon.Weapon):
    def __init__(self, char='s', position=(0, 0)):
        super().__init__(char, position)
        self.state = DefaultParryWeaponState(self)
        self.damage = 3
        self.name = 'sword'
        self.verb = 'slashes'
        self.parry_chance = 1 / 3

registry.Registry.register(Sword, 'weapon', 'common')


class DefaultParryWeaponState(weapon.WeaponState):
    def __init__(self, weapon):
        super().__init__(weapon)
        self.weapon = weapon

    @property
    def parry_chance(self):
        if hasattr(self.weapon, 'parry_chance'):
            return self.weapon.parry_chance

        return 0

    def allow_attack(self, action):
        if random.random() <= self.parry_chance:
            ani = animation.FlashBackground(bg=palette.BRIGHT_YELLOW)
            self.weapon.parent.append(ani)

            instances.console.print('{} parries {}\'s attack!'.format(action.target.display_string,
                                                                      action.performer.display_string))
            return False

        return True
