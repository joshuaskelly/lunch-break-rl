import inspect


class Action(object):
    __base_classes = ()

    def __init__(self):
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
    """A skip op action. Useful for creating hierarchical actions."""
    def perform(self, owner):
        # Perform the next action
        owner.brain.perform_action()


class IdleAction(Action):
    """A no-op action. Useful for timing."""
    def prerequisite(self, owner):
        return True
