import tdl

import instances
import palette
import utils
from ai import brain
from ai.actions import attackaction
from ai.actions import swappositionaction
from entities import animation
from entities import entity
from entities import item
from entities.items.weapons import fist


class Creature(entity.Entity):
    def __init__(self, char, position=(0, 0), fg=(255, 255, 255), bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)
        self.brain = brain.Brain(self)
        self.name = 'Creature'
        self.current_health = 10
        self.max_health = 10
        self.held_item = None
        self.visible_tiles = set()
        self.state = 'NORMAL'
        self.sight_radius = 7.5

        self.equip_held_item(fist.Fist())

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
        if action_to_perform and action_to_perform.prerequisite(self):
            action_to_perform.perform(self)

            # Because we have bumped, cancel our move action
            next_action = self.brain.actions[0] if self.brain.actions else None
            if next_action and \
                not action_to_perform.isinstance('SwapPositionAction') and \
                next_action.isinstance('MoveAction') and \
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

    def equip_held_item(self, new_item):
        self.held_item = new_item
        self.held_item.hidden = True
        self.append(new_item)

    def drop_held_item(self):
        if self.held_item.__class__.__name__ != 'Fist':
            i = self.held_item
            i.remove()
            i.hidden = False
            i.position = self.position
            instances.scene_root.append(i)
            self.held_item = fist.Fist()

    def on_hit(self, action, action_context={}):
        damage_dealt = action_context.get('damage') if 'damage' in action_context else 0
        self.current_health -= damage_dealt
        ani = animation.FlashBackground(bg=palette.BRIGHT_RED)
        self.append(ani)

        if self.current_health > 0 and hasattr(self.held_item, 'on_hurt'):
            self.held_item.on_hurt(damage_dealt, action)

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
        if self.isinstance('Player') and other.isinstance('Player'):
            return swappositionaction.SwapPositionAction(self)

        direction = utils.math.sub(self.position, other.position)
        return attackaction.AttackAction(direction)

    @property
    def visible_entities(self):
        current_scene = instances.scene_root
        result = []

        for e in current_scene.children:
            if not e.isinstance('Entity'):
                continue

            if e == self:
                continue

            if e.position in self.visible_tiles:
                result.append(e)

        return result
