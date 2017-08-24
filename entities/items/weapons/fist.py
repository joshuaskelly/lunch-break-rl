import palette

from entities.items import weapon


class Fist(weapon.Weapon):
    def __init__(self, char='f', position=(0, 0)):
        super().__init__(char, position, fg=palette.BRIGHT_WHITE)

        self.damage = 1
        self.verb = 'punches'
        self.chance_to_break = 0

    def on_use(self):
        pass
