import inspect

import instances
import palette
import utils


class Entity(object):
    __base_classes = ()

    def __init__(self, char, position=(0, 0), fg=palette.BRIGHT_WHITE, bg=palette.BLACK):
        self.position = position
        self.char = char
        self.fg = fg
        self.bg = bg
        self.name = self.__class__.__name__.lower()
        self._children = []
        self.hidden = False
        self.always_show = False
        self.parent = None
        self.blocks_visibility = False
        self.fog_color = None

        if not self.__base_classes:
            self.__base_classes = tuple([c.__name__ for c in inspect.getmro(self.__class__) if c is not object])

    def isinstance(self, cls):
        """Returns if this entity is an instance of the given class

        cls: A string, an instance, or a type
        """
        if isinstance(cls, str):
            pass

        elif type(cls) is type:
            cls = cls.__name__

        else:
            cls = cls.__class__.__name__

        return cls in self.__base_classes

    @property
    def display_string(self):
        return '<color fg="{}">{}</color>'.format(self.fg, self.name)

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

        elif self.fog_color and  self.position in instances.scene_root.level.seen_tiles:
            console.draw_char(*self.offset, self.char, self.fog_color, self.bg)

        for child in self.children:
            child.draw(console)

    def early_update(self, time):
        """Perform per frame logic.

        time: Time elapsed since last update in seconds.
        """
        for child in self.children:
            child.early_update(time)

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

        if parent and child in parent._children:
            parent._children.remove(child)
            child.parent = None
            child.position = None

    def get_action(self, requester=None):
        """Returns an action

        requester: An entity that is requesting the action. Usually this is
            because it wants to perform an action on this entity.

        Returns: An Action or None
        """
        return None

    @property
    def visible(self):
        if self.always_show:
            return True

        if self.hidden:
            return False

        if not self.position:
            return False

        return self.offset in instances.scene_root.level.visible_tiles

    # Implements AttackActionInterface
    def can_attack(self, target):
        """Determines if performer can attack target

        target: An entity
        """
        return True

    def allow_attack(self, action):
        """Determines if target will allow attack"""
        return True

    def before_attacked(self, action):
        """Called on target before attack occurs"""

    def on_attacked(self, action):
        """Called on target to handle being attacked"""

    def after_attacked(self, action):
        """Called on target after attack has occurred"""

    def before_attack(self, action):
        """Called on performer before attack occurs"""

    def after_attack(self, action):
        """Called on performer after attack has occurred"""

    # Implements ThrowActionInterface
    def can_throw(self, target):
        """Determine if performer can throw target"""
        return utils.is_next_to(self, target)

    def allow_throw(self, action):
        """Determine if target allows throw"""
        return True

    # Implements EquipItemInterface
    def can_equip(self, target):
        return self.weapon.isinstance('Fist')
