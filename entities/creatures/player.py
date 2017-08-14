import instances
import game
import helpers
import palette
import utils

from ai import action

from ai.actions import attackaction
from ai.actions import throwaction

from entities import creature


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
        moves = [m for m in moves if m in helpers.DirectionHelper.valid_moves]
        if not moves:
            return

        batched_move = action.BatchedAction(self)

        for command in moves:
            move_action = helpers.MoveHelper.move_to_action(self, command)

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
                    # Moves can be either a series of moves (eg. ULDR) or a
                    # players name
                    moves = ''.join(commands[1:])
                    if moves and moves[0] == '@':
                        moves = moves[1:]

                    players = instances.scene_root.players
                    target = [p for p in players if p.name == moves.lower()]
                    target = target[0] if target else None

                    if target and target is not self:
                        path = instances.scene_root.level.player_pathfinder.get_path(*self.position, *target.position)[:-1]
                        moves = helpers.MoveHelper.path_to_moves(self.position, path)

                    self.queue_batched_move(moves)

                elif commands[0].upper() == '!ATTACK' or commands[0].upper() == '!AT':
                    moves = ''.join(commands[1:])
                    moves = [helpers.DirectionHelper.get_direction(m) for m in moves if m in helpers.DirectionHelper.valid_moves]

                    if moves:
                        batched_attack = action.BatchedAction(self)

                        for attack_dir in moves:
                            act = attackaction.AttackAction(self, direction=attack_dir)
                            act.parent = batched_attack
                            self.brain.add_action(act)

                        self.brain.add_action(batched_attack)

                elif commands[0].upper() == '!DROP':
                    self.drop_held_item()
                    self._has_taken_action = True

                elif commands[0].upper() == '!THROW':
                    direction = commands[1] if len(commands) > 1 else None
                    direction = helpers.DirectionHelper.get_direction(direction[0])

                    if not direction:
                        return

                    target_entity = None
                    dest = utils.math.add(self.position, direction)

                    es = [e for e in instances.scene_root.children if e.isinstance('Entity') and e.position == dest]

                    if es:
                        target_entity = es[0]

                    if target_entity:
                        act = throwaction.ThrowAction(self, target_entity)
                        self.brain.actions.append(act)
                        self._has_taken_action = True

                elif commands[0].upper() == '!STAIRS' and game.Game.args.debug:
                    stair = instances.scene_root.downward_stair
                    path = instances.scene_root.level.player_pathfinder.get_path(self.x, self.y, stair.x, stair.y)
                    moves = helpers.MoveHelper.path_to_moves(self.position, path)
                    self.queue_batched_move(moves)

                elif commands[0].upper() == '!STOP':
                    next_action = self.brain.actions[0] if self.brain.actions else None

                    if next_action and next_action.isinstance('MoveAction'):
                        next_action.fail()
