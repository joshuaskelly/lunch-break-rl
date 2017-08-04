import instances

from ui import window


class Console(window.Window):
    instance = None

    def __init__(self, x, y, width, height, title='Players'):
        super().__init__(x, y, width, height, title)

        self.messages = []

        if not Console.instance:
            Console.instance = self
            instances.register('console', self)

    def print(self, message):
        self.messages.append(message[:self.width-2])

    def draw(self, console):
        super().draw(console)

        row = 1
        for message in self.messages[-self.height+2:]:
            self.data.draw_str(1, row, message)
            row += 1

        console.blit(self.data, self.x, self.y)

    def handle_events(self, event):
        pass
