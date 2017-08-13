import palette
import registry

from entities.items import weapon


class Sword(weapon.Weapon):
    def __init__(self, char='s', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.damage = 3
        self.name = 'sword'
        self.verb = 'slashes'

registry.Registry.register(Sword, 'weapon', 'common')