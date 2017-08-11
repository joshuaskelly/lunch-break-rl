import random

import tdl

import helpers
import instances
import utils

from entities import animation
from entities import creature
from entities import item
from entities import player


class Action(object):
    def __init__(self):
        self.parent = None

    def prerequisite(self, owner):
        return True

    def perform(self, owner):
        pass

    def fail(self, owner):
        if self.parent:
            while owner.brain.actions and owner.brain.actions[0] != self.parent:
                owner.brain.actions.pop(0)

            if self.parent == owner.brain.actions[0]:
                parent_action = owner.brain.actions.pop(0)
                parent_action.fail(owner)

            else:
                raise RuntimeError('Failed to find action parent')


class BatchedAction(Action):
    def perform(self, owner):
        # Perform the next action
        owner.brain.perform_action()


class PerformHeldItemAction(Action):
    def __init__(self, target):
        super().__init__()
        self.target = target

    def prerequisite(self, owner):
        return True

    def perform(self, owner):
        held_action = owner.held_item.move_to_action(owner)


class AttackAction(Action):
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


class MoveAction(Action):
    def __init__(self, direction):
        super().__init__()
        self.direction = direction

    def prerequisite(self, owner):
        return owner.can_move(*self.direction)

    def perform(self, owner):
        owner.move(*self.direction)


class MoveToAction(Action):
    def __init__(self, destination, max_moves=None):
        super().__init__()
        self.destination = destination
        self.max_moves = int(max_moves)

    def prerequisite(self, owner):
        scene_root = instances.scene_root
        level = scene_root.level

        return self.destination in level.data and scene_root.check_collision(*self.destination)

    def perform(self, owner):
        path = instances.scene_root.level.pathfinder.get_path(*owner.position, *self.destination)

        if self.max_moves:
            path = path[:self.max_moves]

        moves = helpers.MoveHelper.path_to_moves(owner.position, path)

        if not moves:
            return

        batched_move = BatchedAction()
        first_move = None

        for command in moves:
            move_action = helpers.MoveHelper.move_to_action(command)

            if move_action:
                move_action.parent = batched_move
                owner.brain.add_action(move_action)

                if not first_move:
                    first_move = move_action

        owner.brain.add_action(batched_move)

        if owner.brain.actions[0] is first_move:
            owner.brain.perform_action()


class WanderAction(Action):
    def prerequisite(self, owner):
        return True

    def perform(self, owner):
        moves = (1, 0), (-1, 0), (0, 1), (0, -1)

        number_of_moves = random.randint(1, 3)
        batched_move = BatchedAction()

        for _ in range(number_of_moves):
            move_action = MoveAction(moves[random.randint(0, 3)])
            move_action.parent = batched_move
            owner.brain.add_action(move_action)

        owner.brain.add_action(batched_move)


class IdleAction(Action):
    def prerequisite(self, owner):
        return True

    def perform(self, owner):
        pass


class EquipItemAction(Action):
    def __init__(self, item):
        super().__init__()
        self.item = item

    def prerequisite(self, owner):
        return True

    def perform(self, owner):
        old_item = owner.held_item
        old_item.position = self.item.position
        old_item.remove()
        old_item.hidden = False

        owner.held_item = self.item
        self.item.remove()
        self.item.hidden = True
        owner.append(self.item)

        if old_item and not isinstance(old_item, item.Fist):
            if old_item.parent:
                old_item.parent.remove(old_item)

            instances.scene_root.level.append(old_item)

        if owner.visible:
            instances.console.print('{} is equiping {}'.format(owner.name, self.item.name))


class UseItemAction(Action):
    def __init__(self, item):
        super().__init__()
        self.item = item

    def prerequisite(self, owner):
        return True

    def perform(self, owner):
        self.item.use(owner)
        self.item.remove()


class ThrowAction(Action):
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
                    if isinstance(hit_entity, creature.Creature):
                        if isinstance(thrown_entity, item.HeldItem):
                            # Have player equip thrown_entity item
                            if isinstance(hit_entity, player.Player) and hit_entity.held_item is None:
                                act = thrown_entity.get_action(owner)
                                action_to_perform = act.perform
                                target_entity = hit_entity

                            # Perform an attack roll otherwise
                            else:
                                act = hit_entity.get_action(owner)
                                action_to_perform = act.perform
                                target_entity = hit_entity

                        # Use potion on target player
                        elif isinstance(thrown_entity, item.UsableItem):
                            action_to_perform = thrown_entity.use
                            target_entity = hit_entity

                        done = True
                        break

            if done:
                break

            dest = point

        if isinstance(thrown_entity, creature.Creature):
            # Cancel any pending actions
            target_next_action = self.target.brain.actions[0] if self.target.brain.actions else None
            if target_next_action:
                target_next_action.fail(self.target)

        if isinstance(target_entity, creature.Creature):
            # Do something?
            pass

        ani = animation.ThrowMotion(thrown_entity.position, dest, 1.0)
        thrown_entity.append(ani)
        thrown_entity.position = dest

        def action_callback():
            if action_to_perform:
                action_to_perform(target_entity)

            if owner.visible:
                instances.console.print('{} {} {}'.format(owner.name, 'throws', thrown_entity.name))

        ani.on_done = action_callback


class SwapPosition(Action):
    def __init__(self, target):
        self.target = target

    def prerequisite(self, owner):
        return utils.is_next_to(owner, self.target)

    def perform(self, owner):
        self.target.position = owner.position

        # Cancel any pending actions
        if isinstance(self.target, creature.Creature):
            target_next_action = self.target.brain.actions[0] if self.target.brain.actions else None
            if target_next_action:
                target_next_action.fail(self.target)
