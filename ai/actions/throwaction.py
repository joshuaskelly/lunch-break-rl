import tdl

import instances
import utils
from ai import action
from entities import animation


class ThrowAction(action.Action):
    def __init__(self, target):
        super().__init__()
        self.target = target

    def prerequisite(self, owner):
        return utils.is_next_to(owner, self.target)

    def perform(self, owner):
        self.owner = owner
        thrown_entity = self.target

        weapon = owner.held_item
        weapon_range = 3

        if hasattr(weapon, 'range'):
            weapon_range = weapon.range

        # Determine direction of throw
        dx, dy = utils.math.sub(thrown_entity.position, owner.position)
        dest = thrown_entity.position

        # Determine destination of throw
        if dx != 0:
            dest = dest[0] + dx * weapon_range, dest[1]

        elif dy != 0:
            dest = dest[0], dest[1] + dy * weapon_range

        path = tdl.map.bresenham(*thrown_entity.position, *dest)
        dest = thrown_entity.position
        action_to_perform = None
        target_entity = None

        current_scene = instances.scene_root
        done = False
        for point in path[1:]:
            if current_scene.is_solid(*point):
                break

            entities = current_scene.get_entity_at(*point)
            if entities:
                for hit_entity in entities:
                    if hit_entity.isinstance('Creature'):
                        if thrown_entity.isinstance('HeldItem'):
                            # Have player equip thrown_entity item
                            if hit_entity.isinstance('Player') and hit_entity.held_item is None:
                                act = thrown_entity.get_action(owner)
                                action_to_perform = act.perform
                                target_entity = hit_entity

                            # Perform an attack roll otherwise
                            else:
                                act = hit_entity.get_action(owner)
                                action_to_perform = act.perform
                                target_entity = hit_entity

                        # Use potion on target player
                        elif thrown_entity.isinstance('UsableItem'):
                            action_to_perform = thrown_entity.use
                            target_entity = hit_entity

                        done = True
                        break

            if done:
                break

            dest = point

        if thrown_entity.isinstance('Creature'):
            # Cancel any pending actions
            target_next_action = self.target.brain.actions[0] if self.target.brain.actions else None
            if target_next_action:
                target_next_action.fail(self.target)

        ani = animation.ThrowMotion(thrown_entity.position, dest, 0.25)
        thrown_entity.append(ani)
        thrown_entity.hidden = True
        thrown_entity.position = dest

        def action_callback():
            if action_to_perform:
                action_to_perform(target_entity)

            if owner.visible:
                instances.console.print('{} {} {}'.format(owner.name, 'throws', thrown_entity.name))

        ani.on_done = action_callback
