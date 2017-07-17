import random

import scene

from entities import item
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
        held_action = owner.held_item.get_action()


class AttackAction(Action):
    def __init__(self, target):
        super().__init__()
        self.target = target

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

        weapon = owner.held_item
        damage_dealt = 1
        verb = 'attacks'
        if weapon:
            if hasattr(weapon, 'damage'):
                damage_dealt = weapon.damage

            if hasattr(weapon, 'verb'):
                verb = weapon.verb

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
