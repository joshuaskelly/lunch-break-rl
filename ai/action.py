class Action(object):
    def __init__(self):
        self.parent = None

    def prerequisite(self, owner):
        return True

    def perform(self, owner):
        pass

    def fail(self, owner):
        if self.parent:
            while owner.brain.actions and owner.brain.actions[0] != self.parent:
                owner.brain.actions.pop(0)

            if self.parent == owner.brain.actions[0]:
                parent_action = owner.brain.actions.pop(0)
                parent_action.fail(owner)

            else:
                raise RuntimeError('Failed to find action parent')


class BatchedAction(Action):
    def perform(self, owner):
        # Perform the next action
        owner.brain.perform_action()


class PerformHeldItemAction(Action):
    def __init__(self, target):
        super().__init__()
        self.target = target

    def prerequisite(self, owner):
        return True

    def perform(self, owner):
        held_action = owner.held_item.move_to_action(owner)


class IdleAction(Action):
    def prerequisite(self, owner):
        return True

    def perform(self, owner):
        pass
