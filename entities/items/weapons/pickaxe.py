import palette
import registry

from entities.items import weapon


class PickAxe(weapon.Weapon):
    def __init__(self, char='p', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.damage = 2
        self.name = 'pick axe'
        self.verb = 'strikes'

registry.Registry.register(PickAxe, 'weapon', 'uncommon')
