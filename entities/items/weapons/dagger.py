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

    def on_hurt(self, damage, attack_action):
        if hasattr(attack_action, 'tags'):
            if 'counter' in attack_action.tags:
                return

        direction = utils.math.sub(attack_action.performer.position, attack_action.target.position)
        counter = attackaction.AttackAction(attack_action.target, attack_action.performer, direction)
        counter.tags = ['counter']

        if counter.prerequisite():
            instances.console.print('{} counter attacks!'.format(attack_action.target.name))
            counter.perform()

registry.Registry.register(Dagger, 'weapon', 'common')