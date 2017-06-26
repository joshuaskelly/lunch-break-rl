class Action(object):
    def prerequiste(self, owner):
        return True

    def perform(self, owner):
        #DO SOMETHING
        pass


class MoveAction(Action):
    def __init__(self, dest):
        self.dest = dest

    def prerequiste(self, owner):
        return owner.can_move(*self.dest)

    def perform(self, owner):
        if self.prerequiste(owner):
            owner.move(*self.dest)
