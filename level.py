import pickle
import os

import tdl

import palette
import scene

from entities import player

class Level(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.data = tdl.Console(width, height)
        self.painting = False
        self.erasing = False
        self.visible_tiles = set()
        self.seen_tiles = set()

    def draw_char(self, x, y, fg=Ellipsis, bg=Ellipsis):
        self.data.draw_char(x, y, fg, bg)

    def get_char(self, x, y):
        return self.data.get_char(x, y)

    def draw(self, console):
        for x, y in self.data:
            ch, fg, bg = self.data.get_char(x, y)
            x += self.x
            y += self.y

            if (x, y) in self.seen_tiles:
                if (x, y) in self.visible_tiles:
                    fg = palette.WHITE

                else:
                    fg = palette.BRIGHT_BLACK

                console.draw_char(x, y, ch, fg, bg)

    def handle_events(self, event):
        if event.type == 'MOUSEDOWN':
            if event.button == 'LEFT':
                if not self.erasing:
                    self.painting = True

            if event.button == 'RIGHT':
                if not self.painting:
                    self.erasing = True

        if event.type == 'MOUSEUP':
            if event.button == 'LEFT':
                if not self.erasing:
                    self.painting = False

            if event.button == 'RIGHT':
                if not self.painting:
                    self.erasing = False

        if event.type == 'MOUSEMOTION':
            pos = event.cell
            pos = pos[0] - self.x, pos[1] - self.y

            if pos in self.data:
                if self.painting:
                    self.draw_char(*pos, '#')

                elif self.erasing:
                    self.draw_char(*pos, ' ')


            if event.type == 'KEYDOWN':
                if event.keychar.upper() == 'S':
                    self.save()

                elif event.keychar.upper() == 'L':
                    self.load()

    def save(self):
        print('Saving Level Data')
        data = [self.data.get_char(*i) for i in self.data]
        binary_data = pickle.dumps(data)
        with open('map.dat', 'wb') as file:
            file.write(binary_data)

    def load(self):
        if not os.path.exists('map.dat'):
            print('No Level Data Found to Load')
            return

        print('Loading Level Data')
        with open('map.dat', 'rb') as file:
            binary_data = file.read()

        data = pickle.loads(binary_data)

        for i, t in enumerate(self.data):
            char, fg, bg = data[i]
            self.data.draw_char(*t, chr(char), fg, bg)

    def update(self, time):
        pass

    def update_fov(self):
        current_scene = scene.Scene.current_scene
        self.visible_tiles = set()

        for e in current_scene.entities:
            if not isinstance(e, player.Player):
                continue

            self.visible_tiles = self.visible_tiles.union(e.visible_tiles)
            self.seen_tiles = self.seen_tiles.union(e.visible_tiles)
