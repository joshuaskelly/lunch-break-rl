import random

import tdl

import scene
import utils

from entities import animation
from entities import creature
from entities import item
from entities import player
from ui import console

class Action(object):
    def __init__(self):
        self.parent = None

    def prerequiste(self, owner):
        return True

    def perform(self, owner):
        #DO SOMETHING
        pass

    def fail(self, owner):
        if self.parent:
            while owner.brain.actions[0].parent == self.parent:
                owner.brain.actions.pop(0)

            if self.parent == owner.brain.actions[0]:
                parent_action = owner.brain.actions.pop(0)
                parent_action.on_fail(owner)

    def on_fail(self, owner):
        pass


class BatchedMoveAction(Action):
    pass


class PerformHeldItemAction(Action):
    def __init__(self, target):
        super().__init__()
        self.target = target

    def prerequiste(self, owner):
        return True

    def perform(self, owner):
        held_action = owner.held_item.get_action(owner)


class AttackAction(Action):
    def __init__(self, target):
        super().__init__()
        self.target = target
        self.weapon = None

    def prerequiste(self, owner):
        dx = owner.position[0] - self.target.position[0]
        dy = owner.position[1] - self.target.position[1]

        if abs(dx) > 1:
            return False

        if abs(dy) > 1:
            return False

        if abs(dx) == 1 and abs(dy) == 1:
            return False

        return True

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
            console.Console.current_console.print('{} {} {}'.format(owner.name, verb, self.target.name))

        self.target.hurt(damage_dealt, self)

class MoveAction(Action):
    def __init__(self, dest):
        super().__init__()
        self.dest = dest

    def prerequiste(self, owner):
        return owner.can_move(*self.dest)

    def perform(self, owner):
        owner.move(*self.dest)
        #console.Console.current_console.print('{} is moving'.format(owner.name))


class IdleAction(Action):
    def prerequiste(self, owner):
        return True

    def perform(self, owner):
        moves = (1, 0), (-1, 0), (0, 1), (0, -1)

        number_of_moves = random.randint(1, 3)

        for _ in range(number_of_moves):
            move = MoveAction(moves[random.randint(0, 3)])
            owner.brain.add_action(move)

        owner.brain.add_action(IdleAction())
        #console.Console.current_console.print('{} is thinking...'.format(owner.name))

class EquipItemAction(Action):
    def __init__(self, item):
        super().__init__()
        self.item = item

    def prerequiste(self, owner):
        return True

    def perform(self, owner):
        old_item = owner.held_item
        old_item.position = self.item.position

        owner.held_item = self.item
        self.item.remove()

        if old_item and not isinstance(old_item, item.Fist):
            scene.Scene.current_scene.entities.append(old_item)

        if owner.visible:
            console.Console.current_console.print('{} is equiping {}'.format(owner.name, self.item.name))

class UseItemAction(Action):
    def __init__(self, item):
        super().__init__()
        self.item = item

    def prerequiste(self, owner):
        return True

    def perform(self, owner):
        self.item.use(owner)
        self.item.remove()

class ThrowAction(Action):
    def __init__(self, target):
        super().__init__()
        self.target = target

    def prerequiste(self, owner):
        return utils.is_next_to(owner, self.target)

    def perform(self, owner):
        self.owner = owner
        thrown_entity = self.target

        weapon = owner.held_item
        weapon_range = 3

        if hasattr(weapon, 'range'):
            weapon_range = weapon.range

        # Determine direction of throw
        dx = thrown_entity.position[0] - owner.position[0]
        dy = thrown_entity.position[1] - owner.position[1]
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

        current_scene = scene.Scene.current_scene
        level = current_scene.level
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

        ani = animation.ThrowMotion(thrown_entity, thrown_entity.position, dest, 1.0)
        thrown_entity.children.append(ani)
        thrown_entity.position = dest

        def action_callback():
            if action_to_perform:
                action_to_perform(target_entity)

            if owner.visible:
                console.Console.current_console.print('{} {} {}'.format(owner.name, 'throws', thrown_entity.name))

        ani.on_done = action_callback


class SwapPosition(Action):
    def __init__(self, target):
        self.target = target

    def prerequiste(self, owner):
        return utils.is_next_to(owner, self.target)

    def perform(self, owner):
        self.target.position = owner.position

        # Cancel any pending actions
        if isinstance(self.target, creature.Creature):
            target_next_action = self.target.brain.actions[0] if self.target.brain.actions else None
            if target_next_action:
                target_next_action.fail(self.target)
