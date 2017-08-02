import palette

from ai import action
from entities import entity
from ui import console


class Item(entity.Entity):
    def get_action(self, other=None):
        pass

    def get_special_action(self, target):
        return None


class HeldItem(Item):
    def get_action(self, other=None):
        return action.EquipItemAction(self)

    def get_perform_action(self, target):
        return action.AttackAction(target)


class UsableItem(Item):
    def get_action(self, other=None):
        return action.UseItemAction(self)

    def use(self, target):
        console.Console.current_console.print('{} is being used on {}'.format(self.name, target.name))


class Potion(UsableItem):
    def __init__(self, char='s', position=(0, 0), fg=(255, 255, 255), bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.heal_amount = 4

    def use(self, target):
        console.Console.current_console.print('{} recovers {} health!'.format(target.name, self.heal_amount))
        target.current_health = min(target.max_health, target.current_health + self.heal_amount)


class Fist(HeldItem):
    def __init__(self, char, position=(0, 0), fg=(255, 255, 255), bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.damage = 1
        self.verb = 'punches'


class Sword(HeldItem):
    def __init__(self, char='s', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.damage = 3
        self.name = 'sword'
        self.verb = 'slashes'

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

        counter = action.AttackAction(attacker)
        counter.tags = ['counter']

        if counter.prerequiste(owner):
            console.Console.current_console.print('{} counter attacks!'.format(owner.name))
            counter.perform(owner)

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
