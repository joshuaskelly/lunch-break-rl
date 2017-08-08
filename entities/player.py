import instances
import palette
import utils

from ai import action
from entities import creature
from entities import entity


class Player(creature.Creature):
    def __init__(self, char='@', position=(0, 0), fg=palette.BRIGHT_RED, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)
        self.name = 'Player'
        self._last_action_tick = 0
        self._current_tick = 999999
        self._has_taken_action = False

    def update(self, time):
        super().update(time)

    def tick(self, tick):
        super().tick(tick)

        self._current_tick = tick

        if self._has_taken_action or self.state == 'EXITED':
            self._last_action_tick = tick
            self._has_taken_action = False

    def draw(self, console):
        if self.state != 'EXITED':
            super().draw(console)

    @property
    def idle(self):
        return self._current_tick - self._last_action_tick > 30

    def move(self, x, y):
        super().move(x, y)

    def handle_events(self, event):
        super().handle_events(event)

        if self.state == "EXITED":
            return

        if event.type == 'TWITCHCHATMESSAGE':
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
                            self._has_taken_action = True

                        elif command.upper() == 'D':
                            move = action.MoveAction((0, 1))
                            move.parent = batched_move
                            self.brain.add_action(move)
                            self._has_taken_action = True

                        elif command.upper() == 'L':
                            move = action.MoveAction((-1, 0))
                            move.parent = batched_move
                            self.brain.add_action(move)
                            self._has_taken_action = True

                        elif command.upper() == 'R':
                            move = action.MoveAction((1, 0))
                            move.parent = batched_move
                            self.brain.add_action(move)
                            self._has_taken_action = True

                    self.brain.add_action(batched_move)

                elif commands[0].upper() == '!DROP':
                    self.drop_held_item()
                    self._has_taken_action = True

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

                    es = [e for e in instances.scene_root.children if isinstance(e, entity.Entity) and e.position == dest]

                    if es:
                        target_entity = es[0]

                    if target_entity:
                        act = action.ThrowAction(target_entity)
                        self.brain.actions.append(act)
                        self._has_taken_action = True

                elif commands[0].upper() == '!STAIRS':
                    stair = instances.scene_root.downward_stair
                    path = instances.scene_root.level.pathfinder.get_path(self.x, self.y, stair.x, stair.y)

                    a = path[:]
                    b = path[:-1]
                    b.insert(0, self.position)
                    z = list(zip(a, b))

                    def func(item):
                        lhs = item[0]
                        rhs = item[1]

                        return utils.math.sub(lhs, rhs)

                    moves = list(map(func, z))

                    t = {
                        (1, 0): 'R',
                        (0, 1): 'D',
                        (-1, 0): 'L',
                        (0, -1): 'U'
                    }

                    moves = [t[i] for i in moves]

                    # TODO: Refactor this UGLY!
                    class FakeTwitchEvent(object):
                        def __init__(self, nick, message):
                            self.type = 'TWITCHCHATMESSAGE'
                            self.nickname = nick
                            self.message = message

                    ev = FakeTwitchEvent(self.name, '!MV {}'.format(''.join(moves)))
                    self.handle_events(ev)
