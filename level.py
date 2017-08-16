import tdl

import game
import instances
import palette
import utils

from entities import entity


class LevelEntity(entity.Entity):
    def __init__(self, position, level):
        self.is_initing = True
        self.__cache = None
        char, fg, bg = level.get_char(*position)
        self.level = level
        super().__init__(char, position, fg, bg)
        self.name = 'wall'
        self.is_initing = False

    @property
    def char(self):
        char, _, _ = self._get_char(*self.position)
        self.__cache = None
        return char

    @char.setter
    def char(self, char):
        if self.is_initing:
            return

        self.level.draw_char(*self.position, char, self.fg, self.bg)
        self.__cache = None

    @property
    def fg(self):
        _, fg, _ = self._get_char(*self.position)
        self.__cache = None
        return fg

    @fg.setter
    def fg(self, fg):
        if self.is_initing:
            return

        self.level.draw_char(*self.position, self.char, fg, self.bg)
        self.__cache = None

    @property
    def bg(self):
        _, _, bg = self._get_char(*self.position)
        self.__cache = None
        return bg

    @bg.setter
    def bg(self, bg):
        self.level.draw_char(*self.position, self.char, self.fg, bg)
        self.__cache = None

    def _get_char(self, x, y):
        if not self.__cache:
            self.__cache = self.level.get_char(x, y)

        return self.__cache

    def on_attacked(self, action):
        if action.performer.weapon.name == 'pick axe':
            self.level.draw_char(self.position[0], self.position[1], '.')
            instances.console.print('{} destroys the wall'.format(action.performer.display_string))

        else:
            instances.console.print('{} {} the wall'.format(action.performer.display_string, action.performer.weapon.verb))


class Level(entity.Entity):
    def __init__(self, x, y, width, height):
        super().__init__(' ', position=(x, y))
        self.width = width
        self.height = height
        self.data = tdl.Console(width, height)
        self.painting = False
        self.erasing = False
        self.visible_tiles = set()
        self.seen_tiles = set()
        self.always_show = True
        self.pathfinder = tdl.map.AStar(width, height, callback=self.move_cost, diagnalCost=0)
        self.player_pathfinder = tdl.map.AStar(width, height, callback=self.player_move_cost, diagnalCost=0)

    def move_cost(self, x, y):
        if (x, y) not in self.data:
            return 0

        ch, fg, bg = self.data.get_char(x, y)
        if ch == ord('.'):
            return 1

        return 0

    def player_move_cost(self, x, y):
        if (x, y) not in self.data:
            return 0

        if (x, y) not in self.seen_tiles:
            return 0

        ch, fg, bg = self.data.get_char(x, y)
        if ch == ord('.'):
            return 1

        return 0

    def draw_char(self, x, y, char, fg=(255, 255, 255), bg=(0, 0, 0)):
        self.data.draw_char(x, y, char, fg, bg)

    def get_char(self, x, y):
        return self.data.get_char(x, y)

    def draw(self, console):
        for x, y in self.data:
            ch, fg, bg = self.data.get_char(x, y)

            if (x, y) in self.seen_tiles or game.Game.args.no_fog == 'true':
                if (x, y) in self.visible_tiles:
                    pass
                    #fg = palette.WHITE
                    #fg = color_table[chr(ch)][True]

                else:
                    fg = palette.get_nearest((95, 87, 79))

                ox, oy = utils.math.add(self.position, (x, y))
                console.draw_char(ox, oy, ch, fg, bg)

        for child in self.children:
            child.draw(console)
