import instances
import game
import palette
import utils

from ai import action
from entities import creature
from entities import entity


class DirectionHelper(object):
    valid_moves = 'u', 'd', 'l', 'r', 'U', 'D', 'L', 'R'
    dir_map = {
        (1, 0): 'R',
        (0, 1): 'D',
        (-1, 0): 'L',
        (0, -1): 'U',
        'R': (1, 0),
        'D': (0, 1),
        'L': (-1, 0),
        'U': (0, -1),
        'r': (1, 0),
        'd': (0, 1),
        'l': (-1, 0),
        'u': (0, -1)
    }

    @staticmethod
    def get_direction(direction):
        return DirectionHelper.dir_map.get(direction)


class MoveHelper(object):
    @staticmethod
    def path_to_moves(start, path):
        # Calculate relative deltas
        a = path[:]
        b = path[:-1]
        b.insert(0, start)
        z = list(zip(a, b))

        def func(item):
            lhs = item[0]
            rhs = item[1]

            return utils.math.sub(lhs, rhs)

        deltas = list(map(func, z))

        # Convert deltas to moves
        moves = [DirectionHelper.get_direction(i) for i in deltas]

        return moves

    @staticmethod
    def move_to_action(move):
        if move in DirectionHelper.dir_map:
            return action.MoveAction(DirectionHelper.get_direction(move.upper()))

        return None


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

    def queue_batched_move(self, moves):
        moves = [m for m in moves if m in DirectionHelper.valid_moves]
        if not moves:
            return

        batched_move = action.BatchedMoveAction()

        for command in moves:
            move_action = MoveHelper.move_to_action(command)

            if move_action:
                move_action.parent = batched_move
                self.brain.add_action(move_action)
                self._has_taken_action = True

        self.brain.add_action(batched_move)

    def handle_events(self, event):
        super().handle_events(event)

        if self.state == "EXITED":
            return

        if event.type == 'TWITCHCHATMESSAGE':
            if event.nickname == self.name:
                commands = event.message.split(' ')

                if commands[0].upper() == '!MOVE' or commands[0].upper() == '!MV':
                    moves = ''.join(commands[1:])

                    players = instances.scene_root.players
                    target = [p for p in players if p.name == moves.lower()]
                    target = target[0] if target else None

                    if target and target is not self:
                        path = instances.scene_root.level.pathfinder.get_path(*self.position, *target.position)[:-1]
                        moves = MoveHelper.path_to_moves(self.position, path)

                    self.queue_batched_move(moves)

                elif commands[0].upper() == '!DROP':
                    self.drop_held_item()
                    self._has_taken_action = True

                elif commands[0].upper() == '!THROW':
                    direction = commands[1] if len(commands) > 1 else None
                    direction = DirectionHelper.get_direction(direction[0])

                    if not direction:
                        return

                    target_entity = None
                    dest = utils.math.add(self.position, direction)

                    es = [e for e in instances.scene_root.children if isinstance(e, entity.Entity) and e.position == dest]

                    if es:
                        target_entity = es[0]

                    if target_entity:
                        act = action.ThrowAction(target_entity)
                        self.brain.actions.append(act)
                        self._has_taken_action = True

                elif commands[0].upper() == '!STAIRS' and game.Game.args.debug:
                    stair = instances.scene_root.downward_stair
                    path = instances.scene_root.level.pathfinder.get_path(self.x, self.y, stair.x, stair.y)
                    moves = MoveHelper.path_to_moves(self.position, path)
                    self.queue_batched_move(moves)

                elif commands[0].upper() == '!STOP':
                    next_action = self.brain.actions[0] if self.brain.actions else None

                    if isinstance(next_action, action.MoveAction):
                        next_action.fail(self)
