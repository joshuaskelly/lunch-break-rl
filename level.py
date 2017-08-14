import tdl

import game
import palette
import utils

from entities import entity


class LevelEntity(entity.Entity):
    def __init__(self, position, level):
        char, fg, bg = level.get_char(*position)
        super().__init__(char, position, fg, bg)
        self.name = 'wall'
        self.level = level

    def on_attack(self, action):
        if action.performer.weapon.name == 'pick axe':
            self.level.draw_char(self.position[0], self.position[1], '.')


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

            if (x, y) in self.seen_tiles or game.Game.args.no_fog_of_war == 'true':
                if (x, y) in self.visible_tiles:
                    fg = palette.WHITE

                else:
                    fg = palette.BRIGHT_BLACK

                ox, oy = utils.math.add(self.position, (x, y))
                console.draw_char(ox, oy, ch, fg, bg)

        for child in self.children:
            child.draw(console)
