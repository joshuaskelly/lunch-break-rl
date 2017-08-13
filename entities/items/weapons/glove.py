import palette
import registry

from ai.actions import throwaction
from entities.items import weapon


class Glove(weapon.Weapon):
    def __init__(self, char='g', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.name = 'glove'
        self.verb = 'throws'
        self.range = 5

    def get_perform_action(self, target):
        return throwaction.ThrowAction(target)

    def get_special_action(self, target):
        return throwaction.ThrowAction(target)

registry.Registry.register(Glove, 'weapon', 'rare')
