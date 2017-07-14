import scene

class Entity(object):
    def __init__(self, char, position=(0, 0), fg=(255, 255, 255), bg=(0, 0, 0)):
        self.char = char
        self.position = position
        self.fg = fg
        self.bg = bg
        self.name = self.__class__.__name__
        self.children = []

    def draw(self, console):
        if self.position in console:

            if scene.Scene.current_scene.check_visibility(*self.position):
                console.draw_char(*self.position, self.char, self.fg, self.bg)

        for child in self.children:
            child.draw(console)

    def update(self, time):
        for child in self.children:
            child.update(time)

    def handle_events(self, event):
        for child in self.children:
            child.handle_events(event)

    def tick(self):
        pass

    def get_action(self):
        return None

    @property
    def visible(self):
        """Returns True if in Players' visiblity"""
        x, y = self.position
        return (x, y) in scene.Scene.current_scene.level.visible_tiles

    def remove(self):
        if self in scene.Scene.current_scene.entities:
            scene.Scene.current_scene.entities.remove(self)
            self.position = None