import player
import level

class Scene(object):
    current_scene = None

    def __init__(self):
        self.entities = []
        self.entities.append(player.Player())

        self.level = level.Level(40, 30)
        self.level.draw_char(0, 0, '#')

        if not Scene.current_scene:
            Scene.current_scene = self

    def draw(self, console):
        self.level.draw(console)

        for entity in self.entities:
            entity.draw(console)

    def handle_events(self, event):
        for entity in self.entities:
            entity.handle_events(event)

    def check_collision(self, x, y):
        char, fg, bg = self.level.get_char(x, y)
        
        return char == ord('#')
