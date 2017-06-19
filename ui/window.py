import tdl

import draw

class Window(object):
    def __init__(self, x, y, width, height, title=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.data = tdl.Console(0, 0, width, height)

    def update(self):
        draw.box(self.data, 0, 0, self.width - 1, self.height - 1)

    def draw(self, console):
        self.update()
        console.blit(self.data, x, y)