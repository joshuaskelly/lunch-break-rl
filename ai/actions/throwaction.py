import tdl

import instances
import utils
from ai import action
from entities import animation


class ThrowAction(action.Action):
    def __init__(self, performer, target):
        super().__init__(performer, target)

    def prerequisite(self):
        return self.performer.can_throw(self.target) and \
               self.target.allow_throw(self)

    def perform(self):
        weapon = self.performer.weapon
        throw_distance = 3

        if hasattr(weapon, 'throw_distance'):
            throw_distance = weapon.throw_distance

        throw_direction = utils.math.sub(self.target.position, self.performer.position)
        dest = utils.math.add(self.target.position, utils.math.mul(throw_direction, throw_distance))

        path = tdl.map.bresenham(*self.target.position, *dest)
        dest = self.target.position
        action_to_perform = None

        current_scene = instances.scene_root
        done = False
        for point in path[1:]:
            if current_scene.is_solid(*point):
                break

            entities = current_scene.get_entity_at(*point)
            if entities:
                for hit_entity in entities:
                    if hit_entity.isinstance('Creature'):
                        if self.target.isinstance('HeldItem'):
                            act = hit_entity.get_action(self.performer)
                            action_to_perform = act.perform

                        # Use potion on target
                        elif self.target.isinstance('UsableItem'):
                            action_to_perform = self.target.use

                        done = True
                        break
            if done:
                break

            dest = point

        if self.target.isinstance('Creature'):
            # Cancel any pending actions
            self.target.brain.fail_next_action()

        ani = animation.ThrowMotion(self.target.position, dest, 0.25)
        self.target.append(ani)
        self.target.hidden = True
        self.target.position = dest

        def action_callback():
            if action_to_perform:
                action_to_perform()

            if self.performer.visible:
                instances.console.describe(self.performer, '{} {} {}'.format(self.performer.display_string, 'throws', self.target.display_string))

        ani.on_done = action_callback


class ThrowActionInterface(object):
    def can_throw(self, target):
        """Determine if performer can throw target"""
        return True

    def allow_throw(self, action):
        """Determine if target allows throw"""
        return True