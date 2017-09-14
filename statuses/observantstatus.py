import registry

from statuses import status


class ObservantStatus(status.Status):
    def __init__(self, owner):
        super().__init__(owner)
        ObservantStatus.name = 'Observant'
        self.owner_old_sight_radius = owner.sight_radius

    def on_status_begin(self):
        self.owner.sight_radius = self.owner_old_sight_radius + 2

    def on_status_end(self):
        self.owner.sight_radius = self.owner_old_sight_radius

registry.Registry.register(ObservantStatus, 'statuses_drop_table', 3)


class PurblindStatus(status.Status):
    def __init__(self, owner):
        super().__init__(owner)
        PurblindStatus.name = 'Purblind'
        self.owner_old_sight_radius = owner.sight_radius

    def on_status_begin(self):
        self.owner.sight_radius = self.owner_old_sight_radius - 2

    def on_status_end(self):
        self.owner.sight_radius = self.owner_old_sight_radius

registry.Registry.register(PurblindStatus, 'statuses_drop_table', 3)
