import random

import registry

from entities import creature
from statuses import status


class SleepStatus(status.Status):
    def __init__(self, owner):
        super().__init__(owner)
        SleepStatus.name = 'Sleep'
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


class SleepyStatus(status.Status):
    def __init__(self, owner):
        super().__init__(owner)
        SleepyStatus.name = 'Sleepy'

    def tick(self, tick):
        if random.random() < 1 / 32:
            self.owner.add_status(SleepStatus(self.owner))

registry.Registry.register(SleepyStatus, 'statuses_drop_table', 3)