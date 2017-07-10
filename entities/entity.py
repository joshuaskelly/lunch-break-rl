import scene

class Entity(object):
    def __init__(self, char, position=(0, 0), fg=(255, 255, 255), bg=(0, 0, 0)):
        self.char = char
        self.position = position
        self.fg = fg
        self.bg = bg
        self.name = self.__class__.__name__

    def draw(self, console):
        if self.position in console:

            if scene.Scene.current_scene.check_visibility(*self.position):
                console.draw_char(*self.position, self.char, self.fg, self.bg)

    def update(self, time):
        pass

    def handle_events(self, event):
        pass

    def tick(self):
        pass

    def get_action(self):
        return None

    def remove(self):
        if self in scene.Scene.current_scene.entities:
            scene.Scene.current_scene.entities.remove(self)