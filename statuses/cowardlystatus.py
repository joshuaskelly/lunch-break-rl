import random

import helpers
import instances
import palette
import registry
import utils

from entities import animation
from entities import creature
from statuses import status

from ai import action
from ai.actions import moveaction
from ai.actions import wanderaction


class CowardlyStatus(status.Status):
    def __init__(self, owner):
        super().__init__(owner)
        CowardlyStatus.name = 'Cowardly'
        self.timer = 30

    def on_status_begin(self):
        self.owner.brain.is_threat = lambda e: not e.isinstance(self.owner.__class__.__name__)
        self.owner.brain.reset = lambda: self.owner.brain.set_state(CowardlyIdleState)
        self.owner.brain.set_state(CowardlyIdleState)

    def on_status_end(self):
        self.owner.brain.reset()

    def tick(self, tick):
        self.timer -= 1

        if self.timer == 0:
            self.remove()


class CravenStatus(CowardlyStatus):
    def __init__(self, owner):
        super().__init__(owner)
        CowardlyStatus.name = 'Craven'

    def tick(self, tick):
        pass


registry.Registry.register(CravenStatus, 'statuses_drop_table', 1.5)


class CowardlyIdleState(creature.CreatureState):
    def __init__(self, brain):
        super().__init__(brain)

    def tick(self, tick):
        # Idle behavior. Wait and wander.
        if not self.brain.actions:
            batched_action = action.BatchedAction(self.owner)

            for _ in range(random.randint(1, 3)):
                idle_action = action.IdleAction(self.owner)
                idle_action.parent = batched_action
                self.brain.add_action(idle_action)

            wander_action = wanderaction.WanderAction(self.owner)
            wander_action.parent = batched_action
            self.brain.add_action(wander_action)

            self.brain.add_action(batched_action)

    def on_threat_spotted(self, threat):
        # Forget whatever we were doing.
        self.brain.fail_next_action()
        self.brain.actions = []
        self.context['threat'] = threat
        self.brain.set_state(CowardlyFleeState)


class CowardlyFleeState(creature.CreatureState):
    def __init__(self, brain):
        super().__init__(brain)
        threats = sorted([b for b in self.brain.threats if b.position], key=lambda t: utils.math.distance(self.owner.position, t.position))
        if threats:
            self.threat = threats[0]
        else:
            self.brain.set_state(CowardlyIdleState)

    def tick(self, tick):
        if self.threat and self.threat.position:
            # Neighboring tiles
            possible_tiles = [utils.math.add(self.owner.position, d) for d in helpers.DirectionHelper.directions]

            # Possible tiles
            possible_tiles = [d for d in possible_tiles if instances.scene_root.check_collision(*d)]

            # Determine furthest tiles
            possible_tiles = sorted(possible_tiles, key=lambda x: utils.math.distance(x, self.threat.position), reverse=True)

            direction = utils.math.sub(possible_tiles[0], self.owner.position)

            act = moveaction.MoveAction(self.owner, direction)
            self.brain.add_action(act)

    def on_threat_lost(self, threat):
        if threat == self.threat:
            self.threat = None
            self.brain.set_state(CowardlyIdleState)

    def on_state_enter(self, prev_state):
        ani = animation.Flash('!', fg=palette.BRIGHT_BLUE, bg=palette.BLACK)
        self.owner.append(ani)
        self.brain.add_action(action.IdleAction(self.owner))

    def on_state_exit(self, next_state):
        ani = animation.Flash('?', fg=palette.BRIGHT_YELLOW, bg=palette.BLACK)
        self.owner.append(ani)
        self.brain.add_action(action.IdleAction(self.owner))
