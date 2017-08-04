from entities import entity


class Scene(entity.Entity):
    def __init__(self):
        super().__init__(' ')

    def draw(self, console):
        for e in self.entities:
            e.draw(console)

    def handle_events(self, event):
        for e in self.entities:
            e.handle_events(event)

    def update(self, time):
        for entity in self.entities:
            entity.update(time)

    @property
    def entities(self):
        return self.children

    @entities.setter
    def entities(self, entities):
        self.children = entities
