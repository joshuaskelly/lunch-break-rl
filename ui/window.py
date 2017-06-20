import tdl

import draw
import palette
from ui import progressbar

class Window(object):
    def __init__(self, x, y, width, height, title=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.data = tdl.Console(width, height)
        self.title = title
        self.children = []

    def update(self):
        draw.box(self.data, 0, 0, self.width, self.height)

        if self.title:
            center_of_box = self.width // 2
            center_of_title = len(self.title) // 2
            x = max(center_of_box - center_of_title, 1)
            self.data.draw_str(x, 0, self.title[:self.width - 2])

        for child in self.children:
            child.update()

    def draw(self, console):
        self.update()
        for child in self.children:
            child.draw(self.data)

        console.blit(self.data, self.x, self.y)

    def handle_events(self, event):
        for child in self.children:
            child.handle_events(event)
