class Brain(object):
    def __init__(self, owner):
        self.owner = owner
        self.actions = []
        self.state = None

    def tick(self, tick):
        self.state.tick(tick)

    def handle_events(self, event):
        self.state.handle_events(event)

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

    def set_state(self, state_class):
        if not self.owner.alive:
            return

        old_state = self.state
        new_state = state_class(self)

        if old_state:
            old_state.on_state_exit(new_state)

        self.state = new_state
        self.state.on_state_enter(old_state)

    def clear(self):
        self.actions = []

    def reset(self):
        # Potentially set a default state here
        self.clear()
