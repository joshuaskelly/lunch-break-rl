import random

import helpers
import instances
import palette
import utils

from ai import action
from ai import brain
from ai.actions import wanderaction
from ai.actions import moveaction
from ai.actions import movetoaction

from entities import animation
from entities import creature
from entities.items.weapons import dagger


class Monster(creature.Creature):
    def __init__(self, char='K', position=(0, 0), fg=palette.BRIGHT_GREEN,
                 bg=palette.BLACK):
        super().__init__(char, position, fg, bg)
        self.max_health = 4
        self.current_health = self.max_health
        self.name = 'monster'
        self.brain = MonsterBrain(self)
        self.sight_radius = 3.5

        if random.random() <= 1 / 5:
            self.equip_weapon(dagger.Dagger())


class MonsterBrain(brain.Brain):
    def __init__(self, owner):
        super().__init__(owner)
        self.state = None
        self.context = {'threats': []}
        self.set_state(MonsterIdleState)
        self.last_health = owner.current_health
        self.wounded_threshold = 2

    @property
    def threats(self):
        return self.context.get('threats')

    @threats.setter
    def threats(self, value):
        self.context['threats'] = value

    def tick(self, tick):
        if not self.owner.alive:
            return

        # Check if critically hurt
        if self.last_health > self.wounded_threshold >= self.owner.current_health:
            self.on_wounded()

        elif self.last_health <= self.wounded_threshold < self.owner.current_health:
            self.on_no_longer_wounded()

        self.last_health = self.owner.current_health

        # Check for threats
        current_threats = self.get_threats()
        for threat in current_threats:
            if threat not in self.threats:
                self.threats.append(threat)
                self.state.on_threat_spotted(threat)

        for threat in self.threats:
            if threat not in current_threats:
                self.threats.remove(threat)
                self.state.on_threat_lost(threat)

        self.state.tick(tick)

    def get_threats(self):
        return [e for e in self.owner.visible_entities if self.is_threat(e)]

    def is_threat(self, entity):
        return entity.isinstance('Player') and entity.alive

    def on_wounded(self):
        self.state.on_wounded()

    def on_no_longer_wounded(self):
        self.state.on_no_longer_wounded()

    def set_state(self, state_class):
        if not self.owner.alive:
            return

        old_state = self.state
        new_state = state_class(self)

        if old_state:
            old_state.on_state_exit(new_state)

        self.state = new_state
        self.state.on_state_enter(old_state)


class MonsterState(object):
    """State base class"""

    def __init__(self, brain):
        self.brain = brain

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def context(self):
        if self.brain:
            return self.brain.context

        return None

    @property
    def owner(self):
        if self.brain:
            return self.brain.owner

        return None

    def tick(self, tick):
        """Performs per tick logic"""
        pass

    def on_threat_spotted(self, threat):
        """Called when a threatening entity is in sight"""
        pass

    def on_threat_lost(self, threat):
        """Called when a threatening entity is no longer in sight"""
        pass

    def on_wounded(self):
        """Called when owner is critically wounded"""
        pass

    def on_no_longer_wounded(self):
        """Called when owner is no longer critically wounded"""
        pass

    def on_state_enter(self, prev_state):
        """Called when transitioning to this state

        prev_state: The state object transitioning from
        """
        pass

    def on_state_exit(self, next_state):
        """Called when transitioning from this state

        next_state: The state object transitioning to
        """
        pass


class MonsterIdleState(MonsterState):
    """State class that encapsulates idle behavior"""

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
        self.brain.set_state(MonsterAggroState)

    def on_wounded(self):
        self.brain.set_state(MonsterHurtState)


class MonsterAggroState(MonsterState):
    """State class the encapsulates aggressive behavior"""

    def __init__(self, brain):
        super().__init__(brain)
        self.aggro_counter = 0
        self.aggro_cooldown = 5
        self.threat = sorted(self.brain.threats, key=lambda t: utils.math.distance(self.owner.position, t.position))[0]

    def on_state_enter(self, prev_state):
        ani = animation.Flash('!', fg=palette.BRIGHT_RED, bg=palette.BLACK)
        self.owner.append(ani)
        self.brain.add_action(action.IdleAction(self.owner))

    def on_state_exit(self, next_state):
        if isinstance(next_state, MonsterIdleState):
            ani = animation.Flash('?', fg=palette.BRIGHT_YELLOW, bg=palette.BLACK)
            self.owner.append(ani)
            self.brain.add_action(action.IdleAction(self.owner))

    def tick(self, tick):
        if self.aggro_counter <= 0:
            self.brain.add_action(movetoaction.MoveToAction(self.owner, self.threat.position, self.brain.owner.sight_radius))
            self.aggro_counter = self.aggro_cooldown

        self.aggro_counter -= 1

    def on_threat_lost(self, threat):
        if threat == self.threat:
            self.threat = None
            self.brain.set_state(MonsterIdleState)

    def on_wounded(self):
        self.brain.fail_next_action()
        self.brain.actions = []
        self.brain.set_state(MonsterFleeState)


class MonsterHurtState(MonsterState):
    """Class that encapsulates hurt idle behavior"""

    def __init__(self, brain):
        super().__init__(brain)
        self.brain = brain

    def tick(self, tick):
        if not self.brain.actions:
            # Attempt to heal
            # TODO: Have a more generic way of finding healing items
            corpses = [e for e in self.owner.visible_entities if e.isinstance('Corpse')]
            corpses = sorted(corpses, key=lambda c: utils.math.distance(self.owner.position, c.position))

            target = corpses[0] if corpses else None

            if target:
                act = movetoaction.MoveToAction(self.owner, target.position)
                self.brain.add_action(act)

            # Wander otherwise
            else:
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
        """Called when a threatening entity is in sight"""
        self.brain.set_state(MonsterFleeState)

    def on_no_longer_wounded(self):
        self.brain.set_state(MonsterIdleState)


class MonsterFleeState(MonsterState):
    """Class that encapsulates hurt fleeing behavior"""

    def __init__(self, brain):
        super().__init__(brain)
        self.brain = brain
        self.threat = sorted([b for b in self.brain.threats if b.position], key=lambda t: utils.math.distance(self.owner.position, t.position))[0]

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

    def on_no_longer_wounded(self):
        self.brain.set_state(MonsterAggroState)

    def on_threat_lost(self, threat):
        if threat == self.threat:
            self.threat = None
            self.brain.set_state(MonsterHurtState)

    def on_state_enter(self, prev_state):
        ani = animation.Flash('!', fg=palette.BRIGHT_BLUE, bg=palette.BLACK)
        self.owner.append(ani)
        self.brain.add_action(action.IdleAction(self.owner))

    def on_state_exit(self, next_state):
        if isinstance(next_state, MonsterHurtState):
            ani = animation.Flash('?', fg=palette.BRIGHT_YELLOW, bg=palette.BLACK)
            self.owner.append(ani)
            self.brain.add_action(action.IdleAction(self.owner))
