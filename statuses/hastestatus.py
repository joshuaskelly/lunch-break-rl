import instances

from statuses import status


class HasteStatus(status.Status):
    def __init__(self, owner, turns_per_tick=4):
        self.owner = owner
        self.counter = 400
        self.turn_length = instances.game.seconds_per_tick
        self.turns_per_tick = turns_per_tick
        self.t = self.turn_length / turns_per_tick
        self.current_sub_tick = 0

    def update(self, time):
        sub_tick = instances.game.time_since_start // self.t
        if sub_tick != self.current_sub_tick:
            if sub_tick % self.turns_per_tick:
                self.owner.brain.perform_action()

            self.current_sub_tick = sub_tick

    def tick(self, tick):
        self.counter -= 1

        if self.counter == 0:
            self.remove()