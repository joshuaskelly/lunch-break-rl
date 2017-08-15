import tdl

import instances
import utils

from ai import action


class AttackAction(action.Action):
    def __init__(self, performer, target=None, direction=None):
        super().__init__(performer, target)
        self.weapon = None
        if target and not direction:
            direction = utils.math.sub(target.position, performer.position)

        self.direction = direction

    def prerequisite(self):
        p1 = utils.math.add(self.performer.position, self.direction)
        p2 = utils.math.mul(self.direction, self.performer.weapon.range - 1)
        p2 = utils.math.add(p1, p2)

        entities = instances.scene_root.get_entities_along_path(*p1, *p2)

        self.target = entities[0] if entities else None

        return self.performer.can_attack(self.target) and self.target.allow_attack(self)

    def perform(self):
        self.performer.before_attack(self)
        self.target.before_attacked(self)
        self.target.on_attacked(self)
        self.performer.after_attack(self)
        self.target.after_attacked(self)

        # TODO: When to call this?
        #self.weapon.on_use()


class AttackActionInterface(object):
    def can_attack(self, other):
        """Determines if performer can attack target"""
        return True

    def allow_attack(self, action):
        """Determines if target will allow attack"""
        return True

    def before_attacked(self, action):
        """Called on target before attack occurs"""

    def on_attacked(self, action):
        """Called on target to handle being attacked"""

    def after_attacked(self, action):
        """Called on target after attack has occurred"""
