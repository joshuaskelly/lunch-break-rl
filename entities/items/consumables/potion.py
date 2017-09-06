import instances
import palette
import registry

from entities.items import consumable
from statuses import blindstatus


class Potion(consumable.Consumable):
    def __init__(self, char='!', position=(0, 0), fg=palette.BRIGHT_MAGENTA, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)

        self.heal_amount = 4

    def get_action(self, requester=None):
        if requester.current_health >= requester.max_health:
            return None

        return super().get_action(requester)

    def use(self, target):
        instances.console.describe(target, '{} recovers {} health!'.format(target.display_string, self.heal_amount))
        target.current_health = min(target.max_health, target.current_health + self.heal_amount)

registry.Registry.register(Potion, 'item', 3)


class BlindingPotion(consumable.Consumable):
    def __init__(self, char='!', position=(0, 0), fg=palette.MAGENTA, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)

    def use(self, target):
        target.add_status(blindstatus.BlindStatus(target))

registry.Registry.register(BlindingPotion, 'item', 3)
