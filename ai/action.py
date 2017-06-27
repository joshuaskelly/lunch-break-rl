import random

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


class IdleAction(Action):
    def prerequiste(self, owner):
        return True

    def perform(self, owner):
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
        move = MoveAction((x, y))
        owner.brain.add_action(move)
        owner.brain.add_action(IdleAction())
