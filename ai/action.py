import random

from ui import console

class Action(object):
    def __init__(self):
        self.parent = None

    def prerequiste(self, owner):
        return True

    def perform(self, owner):
        #DO SOMETHING
        pass

    def on_fail(self, owner):
        print('Action failed')


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
        # Check if target is in range?
        return True

    def perform(self, owner):
        self.target.current_health -= 1

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
        owner.held_item = self.item
        self.item.remove()
        console.Console.current_console.print('{} is equipping {}'.format(owner.name, self.item.name))

class UseItemAction(Action):
    def __init__(self, item):
        super().__init__()
        self.item = item

    def prerequiste(self, owner):
        return True

    def perform(self, owner):
        self.item.use(owner)
        self.item.remove()
