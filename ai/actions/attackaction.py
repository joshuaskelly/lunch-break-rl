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
        # TODO: Fix directional attacking
        target_pos = utils.math.add(self.performer.position, self.direction)
        entities = instances.scene_root.get_entity_at(*target_pos)
        self.target = entities[0] if entities else None

        return self.performer.can_attack(self.target) and self.target.allow_attack(self)

    def perform(self):
        self.target.on_attack(self)
        self.target.after_attack(self)

        # TODO: When to call this?
        #self.weapon.on_use()


class AttackActionInterface(object):
    def can_attack(self, other):
        """Determines if performer can attack target"""
        return True

    def allow_attack(self, action):
        """Determines if target will allow attack"""
        return True

    def on_attack(self, action):
        """Called on target to handle being attacked"""
        pass

    def after_attack(self, action):
        """Called on target after attack has occurred"""
        pass
