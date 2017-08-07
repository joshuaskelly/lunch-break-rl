import tdl

import game
import instances
import palette
import utils

from entities import entity
from entities import player


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

    def draw_char(self, x, y, fg=Ellipsis, bg=Ellipsis):
        self.data.draw_char(x, y, fg, bg)

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

    def update_fov(self):
        self.visible_tiles = set()

        for e in self.children:
            if not isinstance(e, player.Player):
                continue

            self.visible_tiles = self.visible_tiles.union(e.visible_tiles)
            self.seen_tiles = self.seen_tiles.union(e.visible_tiles)

        if game.Game.args.no_fog_of_war:
            self.visible_tiles = self.visible_tiles.union([(v[0], v[1]) for v in self.data])
            self.seen_tiles = self.seen_tiles.union([(s[0], s[1]) for s in self.data])
