import random

import instances
import registry

from entities.items import weapon


class Whip(weapon.Weapon):
    def __init__(self, char='w', position=(0, 0)):
        super().__init__(char, position)
        self.state = DefaultDisarmWeaponState(self)
        self.damage = 2
        self.range = 2
        self.name = 'whip'
        self.verb = 'whips'
        self.disarm_chance = 1 / 2

registry.Registry.register(Whip, 'weapon', 'uncommon')


class DefaultDisarmWeaponState(weapon.WeaponState):
    def __init__(self, weapon):
        super().__init__(weapon)
        self.weapon = weapon

    @property
    def disarm_chance(self):
        if hasattr(self.weapon, 'disarm_chance'):
            return self.weapon.disarm_chance

        return 0

    def before_attack(self, action):
        if random.random() <= self.disarm_chance and \
                hasattr(action.target, 'drop_weapon') and \
                not action.target.weapon.isinstance('Fist'):

            instances.console.print('{} disarms {}'.format(action.performer.display_string, action.target.display_string))
            action.target.drop_weapon()
