from ai import action

class Brain(object):
    def __init__(self, owner):
        self.owner = owner
        self.actions = []

    def perform_action(self):
        if self.actions:
            current_action = self.actions.pop(0)
            if current_action.prerequiste(self.owner):
                current_action.perform(self.owner)

            else:
                if current_action.parent and self.actions:
                    while self.actions[0] != current_action.parent:
                        self.actions.pop(0)

                    current_action = self.actions.pop(0)
                    current_action.on_fail(self.owner)

    def add_action(self, new_action):
        if isinstance(new_action, action.Action):
            self.actions.append(new_action)
