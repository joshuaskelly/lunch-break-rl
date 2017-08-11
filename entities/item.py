import random

import instances
import palette
import registry
import utils

from ai import action
from entities import entity
from entities import creature


class Item(entity.Entity):
    def get_action(self, other=None):
        pass

    def get_special_action(self, target):
        return None

    def on_use(self):
        pass


class HeldItem(Item):
    def __init__(self, char, position=(0, 0), fg=(255, 255, 255),  bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)
        self.chance_to_break = 1 / 4

    def get_action(self, other=None):
        if isinstance(other.held_item, Fist):
            return action.EquipItemAction(self)

        return None

    def get_perform_action(self, target):
        direction = utils.math.sub(target.position, self.position)
        return action.AttackAction(direction)

    def on_use(self):
        if random.random() < self.chance_to_break:
            instances.console.print('{} {} breaks!'.format(self.parent.name, self.name))

            if isinstance(self.parent, creature.Creature):
                self.parent.drop_held_item()

            self.remove()


class UsableItem(Item):
    def get_action(self, other=None):
        return action.UseItemAction(self)

    def use(self, target):
        instances.console.print('{} is being used on {}'.format(self.name, target.name))


class Potion(UsableItem):
    def __init__(self, char='!', position=(0, 0), fg=palette.BRIGHT_MAGENTA, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.heal_amount = 4

    def use(self, target):
        instances.console.print('{} recovers {} health!'.format(target.name, self.heal_amount))
        target.current_health = min(target.max_health, target.current_health + self.heal_amount)

registry.Registry.register(Potion, 'item', 'uncommon')


class Fist(HeldItem):
    def __init__(self, char, position=(0, 0), fg=(255, 255, 255), bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.damage = 1
        self.verb = 'punches'

    def on_use(self):
        pass


class Sword(HeldItem):
    def __init__(self, char='s', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.damage = 3
        self.name = 'sword'
        self.verb = 'slashes'

registry.Registry.register(Sword, 'weapon', 'common')


class Dagger(HeldItem):
    def __init__(self, char='d', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.damage = 2
        self.name = 'dagger'
        self.verb = 'stabs'

    def on_hurt(self, damage, hurt_action):
        if hasattr(hurt_action, 'tags'):
            if 'counter' in hurt_action.tags:
                return

        owner = hurt_action.target
        attacker = hurt_action.owner
        direction = utils.math.sub(attacker.position, owner.position)
        counter = action.AttackAction(direction)
        counter.tags = ['counter']

        if counter.prerequisite(owner):
            instances.console.print('{} counter attacks!'.format(owner.name))
            counter.perform(owner)

registry.Registry.register(Dagger, 'weapon', 'common')


class Glove(HeldItem):
    def __init__(self, char='g', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.name = 'glove'
        self.verb = 'throws'
        self.range = 5

    def get_perform_action(self, target):
        return action.ThrowAction(target)

    def get_special_action(self, target):
        return action.ThrowAction(target)

registry.Registry.register(Glove, 'weapon', 'rare')


class PickAxe(HeldItem):
    def __init__(self, char='p', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.damage = 2
        self.name = 'pick axe'
        self.verb = 'strikes'

registry.Registry.register(PickAxe, 'weapon', 'uncommon')
