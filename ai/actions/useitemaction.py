from ai import action


class UseItemAction(action.Action):
    def __init__(self, item):
        super().__init__()
        self.item = item

    def prerequisite(self, owner):
        return True

    def perform(self, owner):
        self.item.use(owner)
        self.item.remove()
