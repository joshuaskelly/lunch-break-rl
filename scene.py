import palette
import player
import level

from entities import item

class Scene(object):
    current_scene = None

    def __init__(self):
        self.entities = []

        self.entities.append(item.Item('!', (10, 10), palette.BRIGHT_MAGENTA))
        self.entities.append(player.Player())
        self.level = level.Level(40, 30)

        if not Scene.current_scene:
            Scene.current_scene = self

    def draw(self, console):
        self.level.draw(console)

        for entity in self.entities:
            entity.draw(console)

    def handle_events(self, event):
        self.level.handle_events(event)

        for entity in self.entities:
            entity.handle_events(event)

    def check_collision(self, x, y):
        char, fg, bg = self.level.get_char(x, y)

        return char == ord('#')
