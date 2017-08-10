import tdl

import instances
import palette

from ai import action
from ai import brain
from entities import animation
from entities import entity
from entities import item
from entities import player


class Creature(entity.Entity):
    def __init__(self, char, position=(0, 0), fg=(255, 255, 255), bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg=(0, 0, 0))
        self.brain = brain.Brain(self)
        self.name = 'Creature'
        self.current_health = 10
        self.max_health = 10
        self.held_item = item.Fist('f')
        self.visible_tiles = set()
        self.state = 'NORMAL'
        self.sight_radius = 7.5

        self.append(self.held_item)
        self.held_item.hidden = True

    def move(self, x, y):
        dest = self.position[0] + x, self.position[1] + y

        action_to_perform = None
        target_entity = None

        es = instances.scene_root.get_entity_at(*dest)

        # Determine bump action
        if es:
            target_entity = es[0]

            # Let special item actions override bumped entity's default action
            action_to_perform = self.held_item.get_special_action(target_entity)

            # Get bumped entity's default action
            if not action_to_perform:
                action_to_perform = target_entity.get_action(self)

        # Perform the action if possible
        if action_to_perform and action_to_perform.prerequiste(self):
            action_to_perform.perform(self)

            # Because we have bumped, cancel our move action
            next_action = self.brain.actions[0] if self.brain.actions else None
            if next_action and \
                not isinstance(action_to_perform, action.SwapPosition) and \
                isinstance(next_action, action.MoveAction) and \
                next_action.parent:

                next_action.fail(self)

        if target_entity and target_entity.position == dest and action_to_perform:
            return

        if self.can_move(x, y):
            self.position = self.position[0] + x, self.position[1] + y

    def can_move(self, x, y):
        dest = self.position[0] + x, self.position[1] + y
        return instances.scene_root.check_collision(*dest)

    def can_see(self, target):
        """Returns true if target entity is in sight"""
        if not target or not target.position:
            return False

        return target.position in self.visible_tiles

    def update(self, time):
        if self.current_health <= 0:
            self.die()

        super().update(time)

    def update_fov(self):
        if not self.position:
            return

        x, y = self.position
        self.visible_tiles = tdl.map.quick_fov(x, y, instances.scene_root.check_collision, radius=self.sight_radius)

    def drop_held_item(self):
        if not isinstance(self.held_item, item.Fist):
            i = self.held_item
            i.position = self.position
            instances.scene_root.children.append(i)
            self.held_item = item.Fist('f')

    def hurt(self, damage, hurt_action):
        self.current_health -= damage
        ani = animation.FlashBackground(bg=palette.BRIGHT_RED)
        self.append(ani)

        if self.current_health > 0 and hasattr(self.held_item, 'on_hurt'):
            self.held_item.on_hurt(damage, hurt_action)

    def die(self):
        self.drop_held_item()
        instances.console.print('{} perishes!'.format(self.name))
        self.remove()

    def tick(self, tick):
        super().tick(tick)

        self.brain.tick(tick)
        self.brain.perform_action()
        self.update_fov()

    def get_action(self, other=None):
        if isinstance(self, player.Player) and isinstance(other, player.Player):
            return action.SwapPosition(self)

        return action.AttackAction(self)

    @property
    def visible_entities(self):
        current_scene = instances.scene_root
        result = []

        for e in current_scene.children:
            if not isinstance(e, entity.Entity):
                continue

            if e == self:
                continue

            if e.position in self.visible_tiles:
                result.append(e)

        return result
