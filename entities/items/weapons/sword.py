import random

import instances
import palette
import registry

from entities.items import weapon


class Sword(weapon.Weapon):
    def __init__(self, char='s', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)
        self.state = DefaultParryWeaponState(self)
        self.damage = 3
        self.name = 'sword'
        self.verb = 'slashes'
        self.parry_chance = 0.5

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
        if random.random() < self.parry_chance:
            instances.console.print('{} parries {}\'s attack!'.format(action.target.name,
                                                                      action.performer.name))
            return False

        return True