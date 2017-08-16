import palette

from entities.items import weapon


class Fist(weapon.Weapon):
    def __init__(self, char='f', position=(0, 0), fg=palette.BRIGHT_WHITE, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)

        self.damage = 1
        self.verb = 'punches'

    def on_use(self):
        pass