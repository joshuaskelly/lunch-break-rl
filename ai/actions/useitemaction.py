from ai import action


class UseItemAction(action.Action):
    def __init__(self, performer, target):
        super().__init__(performer, target)

    def prerequisite(self):
        return True

    def perform(self):
        self.target.use(self.performer)
        self.target.remove()
