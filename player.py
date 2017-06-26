import events
import palette

from ai import action
from entities import character

class Player(character.Character):
    def __init__(self, char='@', position=(0, 0), fg=palette.BRIGHT_RED, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)
        self.nickname = 'Player'

    def update(self, time):
        pass

    def move(self, x, y):
        super().move(x, y)

    def handle_events(self, event):
        super().handle_events(event)

        if event.type == 'KEYDOWN':
            if event.keychar.upper() == 'UP':
                self.brain.add_action(action.MoveAction((0, -1)))

            elif event.keychar.upper() == 'DOWN':
                self.brain.add_action(action.MoveAction((0, 1)))

            elif event.keychar.upper() == 'LEFT':
                self.brain.add_action(action.MoveAction((-1, 0)))

            elif event.keychar.upper() == 'RIGHT':
                self.brain.add_action(action.MoveAction((1, 0)))

        elif event.type == 'TWITCHCHATEVENT':
            if event.nickname == self.nickname:
                commands = event.message.split(' ')
                for command in commands:
                    if command.upper() == '!UP':
                        self.brain.add_action(action.MoveAction((0, -1)))

                    elif command.upper() == '!DOWN':
                        self.brain.add_action(action.MoveAction((0, 1)))

                    elif command.upper() == '!LEFT':
                        self.brain.add_action(action.MoveAction((-1, 0)))

                    elif command.upper() == '!RIGHT':
                        self.brain.add_action(action.MoveAction((1, 0)))
