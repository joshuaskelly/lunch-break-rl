import random

import instances
import palette
import registry

from entities.items import weapon


class Dagger(weapon.Weapon):
    def __init__(self, char='d', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)
        self.state = DefaultCounterWeaponState(self)
        self.damage = 2
        self.name = 'dagger'
        self.verb = 'stabs'
        self.counter_chance = 1 / 2

registry.Registry.register(Dagger, 'weapon', 'common')


class DefaultCounterWeaponState(weapon.WeaponState):
    def __init__(self, weapon):
        super().__init__(weapon)
        self.weapon = weapon

    @property
    def counter_chance(self):
        if hasattr(self.weapon, 'counter_chance'):
            return self.weapon.counter_chance

        return 0

    def allow_attack(self, action):
        return True

    def after_attack(self, action):
        if random.random() < self.counter_chance:
            instances.console.print('{} counters {}\'s attack!'.format(action.target.display_string,
                                                                       action.performer.display_string))
            counter = action.target.weapon.Action(performer=action.target,
                                                  target=action.performer)
            action.target.brain.actions.append(counter)
            action.target.brain.perform_action()
