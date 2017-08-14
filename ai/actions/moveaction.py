from ai import action


class MoveAction(action.Action):
    def __init__(self, performer, direction):
        super().__init__(performer)
        self.direction = direction

    def prerequisite(self):
        if not self.direction:
            return False

        return self.performer.can_move(*self.direction)

    def perform(self):
        self.performer.move(*self.direction)
