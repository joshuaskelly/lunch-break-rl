import instances
import utils

from ai import action


class AttackAction(action.Action):
    def __init__(self, performer, target=None, direction=None):
        super().__init__(performer, target)
        self.weapon = None
        self.direction = direction

        if not direction:
            print('no direction!')

    def prerequisite(self):
        target_pos = utils.math.add(self.performer.position, self.direction)
        entities = instances.scene_root.get_entity_at(*target_pos)
        self.target = entities[0] if entities else None

        if not self.target or not self.performer:
            return False

        return utils.is_next_to(self.performer, self.target)

    def perform(self):
        if not self.weapon:
            self.weapon = self.performer.held_item

        damage_dealt = 1
        verb = 'attacks'

        if hasattr(self.weapon, 'damage'):
            damage_dealt = self.weapon.damage

        if hasattr(self.weapon, 'verb'):
            verb = self.weapon.verb

        if self.performer.visible:
            instances.console.print('{} {} {}'.format(self.performer.name, verb, self.target.name))

        action_context = {
            'damage': damage_dealt,
            'owner': self.performer
        }

        self.target.on_hit(self, action_context)
        self.weapon.on_use()
