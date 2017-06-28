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

class MoveAction(Action):
    def __init__(self, dest):
        super().__init__()
        self.dest = dest

    def prerequiste(self, owner):
        return owner.can_move(*self.dest)

    def perform(self, owner):
        if self.prerequiste(owner):
            owner.move(*self.dest)
            console.Console.current_console.print('{} is moving'.format(owner.name))


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
        console.Console.current_console.print('{} is thinking...'.format(owner.name))
