import tdl

import draw
from entities import entity


class Window(entity.Entity):
    def __init__(self, x, y, width, height, title=''):
        super().__init__(' ', position=(x, y))

        self.width = width
        self.height = height
        self.data = tdl.Console(width, height)
        self.title = title

    def update(self, time):
        for child in self.children:
            child.update(time)

    def draw(self, console):
        self.data.clear()

        draw.box(self.data, 0, 0, self.width, self.height)

        if self.title:
            center_of_box = self.width // 2
            center_of_title = len(self.title) // 2
            x = max(center_of_box - center_of_title, 1)
            self.data.draw_str(x, 0, self.title[:self.width - 2])

        for child in self.children:
            child.draw(self.data)

        console.blit(self.data, self.x, self.y)

    def handle_events(self, event):
        for child in self.children:
            child.handle_events(event)
