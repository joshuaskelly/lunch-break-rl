from ai import action


class MoveAction(action.Action):
    def __init__(self, direction):
        super().__init__()
        self.direction = direction

    def prerequisite(self, owner):
        return owner.can_move(*self.direction)

    def perform(self, owner):
        owner.move(*self.direction)
