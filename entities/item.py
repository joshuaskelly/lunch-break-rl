from ai import action
from entities import entity
from ui import console


class Item(entity.Entity):
    def get_action(self):
        pass


class HeldItem(Item):
    def get_action(self):
        return action.EquipItemAction(self)

    def get_perform_action(self, target):
        return action.AttackAction(target)


class UsableItem(Item):
    def get_action(self):
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


class Sword(HeldItem):
    def __init__(self, char='s', position=(0, 0), fg=(255, 255, 255), bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.damage = 3
        self.name = 'sword'
