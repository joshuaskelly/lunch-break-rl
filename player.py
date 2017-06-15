import events
import palette

from entities import character

class Player(character.Character):
    def __init__(self):
        super().__init__('@', fg=palette.BRIGHT_RED)

        events.Event.subscribe('UPDATE', self.update)

    def update(self):
        pass

    def move(self, x, y):
        super().move(x, y)
        events.Event.notify('UPDATE')

    def handle_events(self, event):
        if event.type == 'KEYDOWN':
            if event.keychar.upper() == 'UP':
                self.move(0, -1)

            elif event.keychar.upper() == 'DOWN':
                self.move(0, 1)

            elif event.keychar.upper() == 'LEFT':
                self.move(-1, 0)

            elif event.keychar.upper() == 'RIGHT':
                self.move(1, 0)
