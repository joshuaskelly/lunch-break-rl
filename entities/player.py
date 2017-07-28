import events
import palette
import scene

from ai import action
from entities import creature
from entities import entity

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

                if commands[0].upper() == '!MOVE' or commands[0].upper() == '!MV':
                    batched_move = action.BatchedMoveAction()
                    moves = ''.join(commands[1:])

                    for command in moves:
                        if command.upper() == 'U':
                            move = action.MoveAction((0, -1))
                            move.parent = batched_move
                            self.brain.add_action(move)

                        elif command.upper() == 'D':
                            move = action.MoveAction((0, 1))
                            move.parent = batched_move
                            self.brain.add_action(move)

                        elif command.upper() == 'L':
                            move = action.MoveAction((-1, 0))
                            move.parent = batched_move
                            self.brain.add_action(move)

                        elif command.upper() == 'R':
                            move = action.MoveAction((1, 0))
                            move.parent = batched_move
                            self.brain.add_action(move)

                    self.brain.add_action(batched_move)

                elif commands[0].upper() == '!DROP':
                    self.drop_held_item()

                elif commands[0].upper() == '!THROW':
                    direction = commands[1:]

                    if not direction:
                        return

                    direction = direction[0]

                    target_entity = None
                    dest = self.position

                    if direction.upper() == 'U':
                        dest = dest[0], dest[1] - 1

                    elif direction.upper() == 'D':
                        dest = dest[0], dest[1] + 1

                    if direction.upper() == 'L':
                        dest = dest[0] - 1, dest[1]

                    if direction.upper() == 'R':
                        dest = dest[0] + 1, dest[1]

                    es = [e for e in scene.Scene.current_scene.entities if isinstance(e, entity.Entity) and e.position == dest]
                    print(es)

                    if es:
                        target_entity = es[0]

                    if target_entity:
                        act = action.ThrowAction(target_entity)
                        self.brain.actions.append(act)
