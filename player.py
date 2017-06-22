import events
import palette

from entities import character

class Player(character.Character):
    def __init__(self, char='@', position=(0, 0), fg=palette.BRIGHT_RED, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)
        self.nickname = 'Player'

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

        elif event.type == 'TWITCHCHATEVENT':
            if event.nickname == self.nickname:
                commands = event.message.split(' ')
                for command in commands:
                    if command.upper() == '!UP':
                        self.move(0, -1)

                    elif command.upper() == '!DOWN':
                        self.move(0, 1)

                    elif command.upper() == '!LEFT':
                        self.move(-1, 0)

                    elif command.upper() == '!RIGHT':
                        self.move(1, 0)
