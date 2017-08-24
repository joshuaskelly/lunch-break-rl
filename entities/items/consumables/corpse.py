import instances
import palette

from entities.items import consumable


class Corpse(consumable.Consumable):
    def __init__(self, former):
        super().__init__('%', fg=palette.BRIGHT_RED)
        self.heal_amount = 2
        self.former = former
        self.alive = True #?

    def get_action(self, requester=None):
        if requester.isinstance('Player') or requester.current_health >= requester.max_health:
            return None

        return super().get_action(requester)

    def use(self, target):
        instances.console.describe(target, '{} devours the {}!'.format(target.display_string, self.display_string))
        target.current_health = min(target.max_health, target.current_health + self.heal_amount)

        # Transfer children
        for child in self.children:
            child.remove()
            target.append(child)