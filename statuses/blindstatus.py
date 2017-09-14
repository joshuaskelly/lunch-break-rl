import instances
import registry

from statuses import status


class BlindStatus(status.Status):
    def __init__(self, owner):
        super().__init__(owner)
        BlindStatus.name = 'Blind'
        self.original_sight_radius = self.owner.sight_radius
        self.timer = 30

    def on_status_begin(self):
        instances.console.describe(self.owner, '{} is blinded!'.format(self.owner.display_string))
        self.owner.sight_radius = 0

    def on_status_end(self):
        instances.console.describe(self.owner, '{} can see again!'.format(self.owner.display_string))
        self.owner.sight_radius = self.original_sight_radius

    def tick(self, tick):
        self.timer -= 1

        if self.timer == 0:
            self.remove()

registry.Registry.register(BlindStatus, 'statuses_drop_table', 1)