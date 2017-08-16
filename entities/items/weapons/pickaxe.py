import registry

from entities.items import weapon


class PickAxe(weapon.Weapon):
    def __init__(self, char='p', position=(0, 0)):
        super().__init__(char, position)

        self.damage = 2
        self.name = 'pick axe'
        self.verb = 'strikes'

registry.Registry.register(PickAxe, 'weapon', 'uncommon')
