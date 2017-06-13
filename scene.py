from player import Player
from level import Level

class Scene(object):
    def __init__(self):
        self.entities = []
        self.entities.append(Player())

        self.level = Level(40, 30)
        self.level.draw_char(0, 0, '#')

    def draw(self, console):
        self.level.draw(console)

        for entity in self.entities:
            entity.draw(console)

    def handle_events(self, event):
        for entity in self.entities:
            entity.handle_events(event)
