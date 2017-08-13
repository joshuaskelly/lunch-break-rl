import instances
import palette
import registry
import utils

from ai.actions import attackaction
from entities.items import weapon


class Dagger(weapon.Weapon):
    def __init__(self, char='d', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)

        self.damage = 2
        self.name = 'dagger'
        self.verb = 'stabs'

    def on_hurt(self, damage, hurt_action):
        if hasattr(hurt_action, 'tags'):
            if 'counter' in hurt_action.tags:
                return

        owner = hurt_action.target
        attacker = hurt_action.owner
        direction = utils.math.sub(attacker.position, owner.position)
        counter = attackaction.AttackAction(direction)
        counter.tags = ['counter']

        if counter.prerequisite(owner):
            instances.console.print('{} counter attacks!'.format(owner.name))
            counter.perform(owner)

registry.Registry.register(Dagger, 'weapon', 'common')