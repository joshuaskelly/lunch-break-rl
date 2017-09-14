import time
import instances
import registry

from statuses import status


class HasteStatus(status.Status):
    def __init__(self, owner, turns_per_tick=2, counter=4):
        super().__init__(owner)
        HasteStatus.name = 'Haste'
        self.owner = owner
        self.counter = counter
        self.turn_length = instances.game.seconds_per_tick
        self.turns_per_tick = turns_per_tick
        self.t = self.turn_length / turns_per_tick
        self.current_sub_tick = 0
        self.start_of_effect = None

    @property
    def time_since_start(self):
        if not self.start_of_effect:
            return -1

        return time.time() - self.start_of_effect

    def stack(self, other):
        self.counter += other.counter

    def update(self, time):
        if not self.start_of_effect:
            return

        sub_tick = self.time_since_start // self.t
        if sub_tick != self.current_sub_tick:
            if sub_tick % self.turns_per_tick:
                self.owner.brain.perform_action()

            self.current_sub_tick = sub_tick

    def tick(self, tick):
        if not self.start_of_effect:
            self.start_of_effect = time.time()

        self.counter -= 1

        if self.counter == 0:
            self.remove()


class HyperStatus(HasteStatus):
    def __init__(self, owner):
        super().__init__(owner, turns_per_tick=2)
        HyperStatus.name = 'Hyper'
        self.owner_current_health = owner.current_health

    def tick(self, tick):
        if not self.start_of_effect:
            self.start_of_effect = time.time()

        if self.owner.current_health < self.owner.current_health:
            self.remove()

registry.Registry.register(HyperStatus, 'statuses_drop_table', 3)
