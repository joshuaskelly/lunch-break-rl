class Brain(object):
    def __init__(self, owner):
        self.owner = owner
        self.actions = []

    def tick(self, tick):
        pass

    def perform_action(self):
        if self.actions:
            current_action = self.actions.pop(0)

            # Make sure our owner is the entity actually doing the action
            if current_action.performer is not self.owner:
                raise RuntimeError('Performing action not as owner!')

            if current_action.prerequisite():
                current_action.perform()

            else:
                current_action.fail()

    def add_action(self, new_action):
        if new_action.isinstance('Action'):
            self.actions.append(new_action)

    def fail_next_action(self):
        if self.actions:
            self.actions[0].fail()

    def clear(self):
        self.actions = []
