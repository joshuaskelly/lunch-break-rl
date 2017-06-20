import tdl

import draw

class Window(object):
    def __init__(self, x, y, width, height, title=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.data = tdl.Console(width, height)
        self.title = title

    def update(self):
        draw.box(self.data, 0, 0, self.width, self.height)

        if self.title:
            center_of_box = self.width // 2
            center_of_title = len(self.title) // 2
            x = max(center_of_box - center_of_title, 1)
            self.data.draw_str(x, 0, self.title[:self.width - 2])

    def draw(self, console):
        self.update()
        console.blit(self.data, self.x, self.y)

    def handle_events(self, event):
        pass
