import instances
import utils


class Entity(object):
    def __init__(self, char, position=(0, 0), fg=(255, 255, 255), bg=(0, 0, 0)):
        self.char = char
        self.position = position
        self.fg = fg
        self.bg = bg
        self.name = self.__class__.__name__
        self._children = []
        self.hidden = False
        self.parent = None

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

    @property
    def offset(self):
        """Offset is the 'Global' position of the Entity relative to it's
        containing Scene. Primarily used for drawing."""
        parent_offset = 0, 0
        if self.parent:
            parent_offset = self.parent.offset

        return utils.math.add(self.position, parent_offset)

    @property
    def children(self):
        return self._children

    def draw(self, console):
        if self.visible:
            console.draw_char(*self.offset, self.char, self.fg, self.bg)

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

    def append(self, child):
        if child.parent:
            raise RuntimeError('Attempting to reparent <{}>'.format(child.__class__.__name__))

        if child not in self.children:
            self._children.append(child)
            child.parent = self

        else:
            raise RuntimeError('Attempting to add child <{}> twice to <{}>'.format(child.__class__.__name__, self.__class__.__name__))

    def remove(self, child=None):
        parent = self
        if not child:
            child = self
            parent = self.parent

        if parent:
            parent._children.remove(child)
            child.parent = None
            child.position = None

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
