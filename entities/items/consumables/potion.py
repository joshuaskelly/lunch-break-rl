import instances
import palette
import registry

from entities.items import consumable


class Potion(consumable.Consumable):
    def __init__(self, char='!', position=(0, 0), fg=palette.BRIGHT_MAGENTA, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)

        self.heal_amount = 4

    def use(self, target):
        instances.console.print('{} recovers {} health!'.format(target.display_string, self.heal_amount))
        target.current_health = min(target.max_health, target.current_health + self.heal_amount)

registry.Registry.register(Potion, 'item', 'uncommon')
