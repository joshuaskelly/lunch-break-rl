import helpers
import instances
import registry
import utils

from ai import action
from ai.actions import attackaction

from entities.items import weapon


class BattleAxe(weapon.Weapon):
    def __init__(self, char='b', position=(0, 0)):
        super().__init__(char, position)
        self.damage = 6
        self.total_damage = 6
        self.name = 'battle axe'
        self.verb = 'chops'

    @property
    def Action(self):
        return BattleAxeAttackAction

registry.Registry.register(BattleAxe, 'weapon', 'uncommon')


class BattleAxeAttackAction(action.Action):
    def __init__(self, performer, target=None, direction=None):
        super().__init__(performer, target)
        self.weapon = None
        if target and not direction:
            direction = utils.math.sub(target.position, performer.position)

        self.direction = direction

        self.sub_actions = []

    def prerequisite(self):
        # Build a list of sub actions

        coords = list(map(lambda x: utils.math.add(x, self.performer.position), helpers.DirectionHelper.directions))
        entities = instances.scene_root.get_entities(coords)

        for entity in entities:
            attack = attackaction.AttackAction(self.performer, target=entity, direction=None)
            self.sub_actions.append(attack)

        self.sub_actions = [a for a in self.sub_actions if a.prerequisite()]

        if len(self.sub_actions) > 0:
            self.performer.weapon.damage = self.performer.weapon.total_damage // len(self.sub_actions)
            return True

        self.performer.weapon.damage = self.performer.weapon.total_damage

        return False

    def perform(self):
        for action in self.sub_actions:
            action.performer.before_attack(action)
            action.target.before_attacked(action)
            action.target.on_attacked(action)
            action.performer.after_attack(action)
            action.target.after_attacked(action)

        # TODO: When to call this?
        #self.weapon.on_use()