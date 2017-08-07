import tdl

from entities import entity


class Scene(entity.Entity):
    def __init__(self, x=0, y=0, width=54, height=30):
        super().__init__(' ')
        self.position = x, y
        self.width = width
        self.height = height

        self.console = tdl.Console(width, height)

    @property
    def offset(self):
        return 0, 0

    def draw(self, console):
        if not self.visible:
            return

        for child in self.children:
            child.draw(self.console)

        console.blit(self.console, self.x, self.y, self.width, self.height)
