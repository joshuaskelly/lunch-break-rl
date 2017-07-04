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

class Fist(HeldItem):
    pass

class Sword(HeldItem):
    pass