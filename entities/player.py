import events
import palette

from ai import action
from entities import creature

class Player(creature.Creature):
    def __init__(self, char='@', position=(0, 0), fg=palette.BRIGHT_RED, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)
        self.name = 'Player'

    def update(self, time):
        super().update(time)

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

        elif event.type == 'TWITCHCHATMESSAGE':
            if event.nickname == self.name:
                commands = event.message.split(' ')
                batched_move = action.BatchedMoveAction()

                for command in commands:
                    if command.upper() == '!UP':
                        move = action.MoveAction((0, -1))
                        move.parent = batched_move
                        self.brain.add_action(move)

                    elif command.upper() == '!DOWN':
                        move = action.MoveAction((0, 1))
                        move.parent = batched_move
                        self.brain.add_action(move)

                    elif command.upper() == '!LEFT':
                        move = action.MoveAction((-1, 0))
                        move.parent = batched_move
                        self.brain.add_action(move)

                    elif command.upper() == '!RIGHT':
                        move = action.MoveAction((1, 0))
                        move.parent = batched_move
                        self.brain.add_action(move)
                
                self.brain.add_action(batched_move)
