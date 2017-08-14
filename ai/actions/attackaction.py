import instances
import utils

from ai import action


class AttackAction(action.Action):
    def __init__(self, direction):
        super().__init__()
        self.target = None
        self.weapon = None
        self.direction = direction

    def prerequisite(self, owner):
        target_pos = utils.math.add(owner.position, self.direction)
        entities = instances.scene_root.get_entity_at(*target_pos)
        self.target = entities[0] if entities else None

        if not self.target or not owner:
            return False

        return utils.is_next_to(owner, self.target)

    def perform(self, owner):
        self.owner = owner

        if not self.weapon:
            self.weapon = owner.held_item

        damage_dealt = 1
        verb = 'attacks'

        if hasattr(self.weapon, 'damage'):
            damage_dealt = self.weapon.damage

        if hasattr(self.weapon, 'verb'):
            verb = self.weapon.verb

        if owner.visible:
            instances.console.print('{} {} {}'.format(owner.name, verb, self.target.name))

        action_context = {
            'damage': damage_dealt,
            'owner': owner
        }

        self.target.on_hit(self, action_context)
        self.weapon.on_use()
