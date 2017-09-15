import random

import helpers
import instances
import palette
import registry
import utils

from entities import animation
from entities.items import weapon


class Spear(weapon.Weapon):
    def __init__(self, char='S', position=(0, 0)):
        super().__init__(char, position)
        self.name = 'spear'
        self.verb = 'stabs'
        self.damage = 2
        self.throw_distance = 5
        self.knockback_chance = 3 / 4
        self.state = DefaultSpearWeaponState(self)

registry.Registry.register(Spear, 'weapon', 3)


class DefaultSpearWeaponState(weapon.WeaponState):
    def __init__(self, weapon):
        super().__init__(weapon)
        self.weapon = weapon
        self.last_position = None

    def tick(self, tick):
        if self.weapon.parent.position == self.last_position:
            self.weapon.state = ReadySpearWeaponState(self.weapon)
            instances.console.describe(self.weapon.parent, '{} readies their spear'.format(self.weapon.parent.display_string))
            ani = animation.FlashBackground(bg=palette.BRIGHT_YELLOW)
            self.weapon.parent.append(ani)

        else:
            self.last_position = self.weapon.parent.position


class ReadySpearWeaponState(weapon.WeaponState):
    def __init__(self, weapon):
        super().__init__(weapon)
        self.weapon = weapon
        self.neighbors = []
        self.last_position = weapon.parent.position

    def tick(self, tick):
        if self.weapon.parent.position != self.last_position:
            self.weapon.state = DefaultSpearWeaponState(self.weapon)
            return

        coords = [utils.math.add(self.weapon.parent.position, d) for d in helpers.DirectionHelper.directions]
        neighbors = instances.scene_root.get_entities(coords)
        neighbors = [n for n in neighbors if n.isinstance('Creature')]

        # Handle engaging entities
        for n in neighbors:
            if n not in self.neighbors:
                self.neighbors.append(n)
                self.on_engaged(n)

        # Handle disegage entities
        for n in self.neighbors:
            if n not in neighbors:
                self.neighbors.remove(n)
                self.on_disengaged(n)

    def on_engaged(self, entity):
        if not entity.isinstance('Creature'):
            return

        wielder = self.weapon.parent

        if wielder.brain.is_threat(entity):
            ani = animation.FlashBackground(bg=palette.BRIGHT_YELLOW)
            self.weapon.parent.append(ani)

            act = self.weapon.Action(performer=wielder, target=entity)
            wielder.brain.perform_action(act)

    def on_disengaged(self, entity):
        pass

    def after_attack(self, action):
        if random.random() < self.weapon.knockback_chance and hasattr(action.target, 'move'):
            dir = utils.math.sub(action.target.position, action.performer.position)
            action.target.move(*dir)
            instances.console.describe(action.target, '{} is knocked back!'.format(action.target.display_string))