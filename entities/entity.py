import instances


class Entity(object):
    def __init__(self, char, position=(0, 0), fg=(255, 255, 255), bg=(0, 0, 0)):
        self.char = char
        self.position = position
        self.fg = fg
        self.bg = bg
        self.name = self.__class__.__name__
        self.children = []
        self.hidden = False

    @property
    def x(self):
        return self.position[0]

    @x.setter
    def x(self, value):
        self.position = value, self.position[1]

    @property
    def y(self):
        return self.position[1]

    @y.setter
    def y(self, value):
        self.position = self.position[0], value

    def draw(self, console):
        if self.visible:
            console.draw_char(*self.position, self.char, self.fg, self.bg)

        for child in self.children:
            child.draw(console)

    def update(self, time):
        """Perform per frame logic.
        
        time: Time elapsed since last update in seconds.
        """
        for child in self.children:
            child.update(time)

    def tick(self, tick):
        """Perform per tick logic.
        
        tick: The total number of ticks that have elapsed since game launch
        """
        for child in self.children:
            child.tick(tick)

    def handle_events(self, event):
        for child in self.children:
            child.handle_events(event)

    def get_action(self, other=None):
        """Returns an action

        other: An entity that is requesting the action. Usually this is
            because it wants to perform an action on this entity.

        Returns: An Action or None
        """
        return None

    @property
    def visible(self):
        if self.hidden:
            return False

        if not self.position:
            return False

        return self.position in instances.scene_root.level.visible_tiles

    def remove(self):
        current_scene = instances.scene_root

        if self in current_scene.entities:
            current_scene.entities.remove(self)
            self.position = None
