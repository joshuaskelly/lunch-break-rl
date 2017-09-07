from entities import creature
from statuses import status


class SleepStatus(status.Status):
    def __init__(self, owner):
        self.owner = owner
        self.timer = 30

    def on_status_begin(self):
        self.owner.brain.set_state(creature.CreatureSleepState)
        self.owner.brain.state.sleep_timer = self.timer

    def on_status_end(self):
        if hasattr(self.owner.brain.state, 'wakeup'):
            self.owner.brain.state.wakeup()

    def tick(self, tick):
        self.timer -= 1

        if self.timer == 0:
            self.remove()
