from entities.items import weapon


class Fist(weapon.Weapon):
    def __init__(self, char='f', position=(0, 0), fg=(255, 255, 255), bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.damage = 1
        self.verb = 'punches'
