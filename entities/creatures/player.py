import instances
import helpers
import palette
import utils

from ai import action
from ai import brain

from ai.actions import throwaction
from ai.actions import swappositionaction

from entities import creature
from entities.items.weapons import fist


class Player(creature.Creature):
    def __init__(self, char='@', position=(0, 0), fg=palette.BRIGHT_RED, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)
        self.name = 'Player'
        self.brain = PlayerBrain(self)
        self.cheer_counter = 0
        self.sight_radius = 4.5

    def update(self, time):
        super().update(time)

    def tick(self, tick):
        super().tick(tick)

    def draw(self, console):
        if self.state != 'PlayerExitedState':
            super().draw(console)

    @property
    def idle(self):
        return self.brain.state.idle

    @property
    def state(self):
        return self.brain.state.name

    def get_action(self, requester=None):
        if requester.isinstance('Player'):
            return swappositionaction.SwapPositionAction(requester, self)

        return super().get_action(requester)

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

        self.brain.add_action(batched_move)

    def exit(self):
        self.brain.set_state(PlayerExitedState)
        self.position = -2, -2


class PlayerBrain(brain.Brain):
    def __init__(self, owner):
        super().__init__(owner)
        self.set_state(PlayerReadyState)

    def reset(self):
        self.set_state(PlayerReadyState)
        self.clear()

    def is_threat(self, entity):
        return not entity.isinstance('Player') and entity.alive


class PlayerReadyState(creature.CreatureState):
    """State class that encapsulates normal player behavior"""

    def __init__(self, brain):
        self.brain = brain
        self.last_action = instances.game.tick_count

    def took_action(self):
        self.last_action = instances.game.tick_count

    @property
    def idle(self):
        return instances.game.tick_count - self.last_action > 30

    def handle_events(self, event):
        if self.owner.state == 'PlayerExitedState':
            return

        if event.type == 'TWITCHCHATMESSAGE':
            if event.nickname == self.owner.name:
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
                        path = instances.scene_root.level.player_pathfinder.get_path(*self.owner.position, *target.position)[:-1]
                        moves = helpers.MoveHelper.path_to_moves(self.owner.position, path)

                    self.owner.queue_batched_move(moves)
                    self.took_action()

                elif commands[0].upper() == '!ATTACK' or commands[0].upper() == '!AT':
                    moves = ''.join(commands[1:])
                    moves = [helpers.DirectionHelper.get_direction(m) for m in moves if m in helpers.DirectionHelper.valid_moves]

                    if moves:
                        batched_attack = action.BatchedAction(self.owner)

                        for attack_dir in moves:
                            act = self.owner.weapon.Action(self.owner, direction=attack_dir)
                            act.parent = batched_attack
                            self.brain.add_action(act)

                        self.brain.add_action(batched_attack)

                    self.took_action()

                elif commands[0].upper() == '!DROP':
                    self.owner.drop_weapon()
                    self.took_action()

                elif commands[0].upper() == '!THROW':
                    direction = commands[1] if len(commands) > 1 else None
                    direction = helpers.DirectionHelper.get_direction(direction[0])

                    if not direction:
                        return

                    dest = utils.math.add(self.owner.position, direction)

                    # Throw entity next to player in given direction
                    for target_entity in instances.scene_root.get_entity_at(*dest):
                        act = throwaction.ThrowAction(self.owner, target_entity)
                        if act.prerequisite():
                            self.brain.add_action(act)
                            return

                    # Throw held weapon in given direction
                    if not self.owner.weapon.isinstance('Fist'):
                        w = self.owner.weapon
                        w.remove()
                        w.position = dest
                        instances.scene_root.append(w)
                        self.owner.equip_weapon(fist.Fist())
                        act = throwaction.ThrowAction(self.owner, w)
                        self.brain.add_action(act)

                    self.took_action()

                elif commands[0].upper() == '!STAIRS' and instances.game.args.debug:
                    stair = instances.scene_root.downward_stair
                    path = instances.scene_root.level.pathfinder.get_path(self.owner.x, self.owner.y, stair.x, stair.y)
                    moves = helpers.MoveHelper.path_to_moves(self.owner.position, path)
                    self.owner.queue_batched_move(moves)

                elif commands[0].upper() == '!STOP':
                    next_action = self.brain.actions[0] if self.brain.actions else None

                    if next_action and next_action.isinstance('MoveAction'):
                        next_action.fail()


class PlayerExitedState(creature.CreatureState):
    """State class that encapsulates normal player behavior"""

    @property
    def idle(self):
        return False
