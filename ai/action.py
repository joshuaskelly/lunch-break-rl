import inspect


class Action(object):
    __base_classes = ()

    def __init__(self, performer, target=None):
        self.performer = performer
        self.target = target
        self.parent = None

        if not self.__base_classes:
            self.__base_classes = tuple([c.__name__ for c in inspect.getmro(self.__class__) if c is not object])

    def isinstance(self, cls):
        """Returns if this entity is an instance of the given class

        cls: A string, an instance, or a type
        """
        if isinstance(cls, str):
            pass

        elif type(cls) is type:
            cls = cls.__name__

        else:
            cls = cls.__class__.__name__

        return cls in self.__base_classes

    def prerequisite(self):
        return True

    def perform(self):
        pass

    def fail(self):
        if self.parent:
            while self.performer.brain.actions and self.performer.brain.actions[0] != self.parent:
                self.performer.brain.actions.pop(0)

            if self.parent == self.performer.brain.actions[0]:
                parent_action = self.performer.brain.actions.pop(0)
                parent_action.fail()

            else:
                raise RuntimeError('Failed to find action parent')


class BatchedAction(Action):
    """A skip op action. Useful for creating hierarchical actions."""
    def perform(self):
        # Perform the next action
        self.performer.brain.perform_action()


class IdleAction(Action):
    """A no-op action. Useful for timing."""
    def prerequisite(self):
        return True
