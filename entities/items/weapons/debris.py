import palette

from entities.items import weapon

from ai.actions import equipitemaction


class Debris(weapon.Weapon):
    def __init__(self, char='%', position=(0, 0)):
        super().__init__(char, position, fg=palette.BRIGHT_YELLOW)

        self.damage = 1
        self.verb = 'hits'
        self.chance_to_break = 0

    def get_action(self, requester=None):
        if requester and not requester.isinstance('Player') and requester.weapon.isinstance('Fist'):
            return equipitemaction.EquipItemAction(requester, self)

        return None
