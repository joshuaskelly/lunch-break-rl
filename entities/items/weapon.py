import palette

from entities import item


class Weapon(item.HeldItem):
    def __init__(self, char='w', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.damage = 3
        self.name = 'weapon'
        self.verb = 'hits'
