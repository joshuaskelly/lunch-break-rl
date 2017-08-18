import random

import helpers
import instances
import palette
import registry
import utils

from ai import action
from ai import brain

from ai.actions import wanderaction
from ai.actions import moveaction
from ai.actions import movetoaction

from entities import animation
from entities import creature
from entities.items.weapons import dagger


class Kobold(creature.Creature):
    def __init__(self, char='K', position=(0, 0), fg=palette.BRIGHT_GREEN, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)
        self.max_health = 4
        self.current_health = self.max_health
        self.name = 'kobold'
        self.brain = KoboldBrain(self)
        self.sight_radius = 3.5

        if random.random() <= 1 / 5:
            self.equip_weapon(dagger.Dagger())

registry.Registry.register(Kobold, 'monster', 'common')


class KoboldBrain(brain.Brain):
    def __init__(self, owner):
        super().__init__(owner)
        self.state = None
        self.context = {'threat': None}
        self.set_state(KoboldIdleState)
        self.last_health = owner.current_health
        self.wounded_threshold = 2

    @property
    def threat(self):
        return self.context.get('threat')

    @threat.setter
    def threat(self, value):
        self.context['threat'] = value

    def tick(self, tick):
        # Check if critically hurt
        if self.last_health > self.wounded_threshold and self.owner.current_health <= self.wounded_threshold:
            self.on_wounded()

        elif self.last_health <= self.wounded_threshold and self.owner.current_health > self.wounded_threshold:
            self.on_no_longer_wounded()

        self.last_health = self.owner.current_health

        # Check for threats
        self.threat = self.get_nearest_threat()
        if self.threat:
            self.state.on_threat_spotted(self.threat)

        if not self.owner.can_see(self.threat):
            self.state.on_threat_lost(self.threat)
            self.threat = None

        self.state.tick(tick)

    def get_nearest_threat(self):
        """Returns the closes visible entity that is a threat"""
        threats = [e for e in self.owner.visible_entities if self.is_threat(e)]
        if threats:
            return threats[0]

        return None

    def is_threat(self, entity):
        return entity.isinstance('Player')

    def on_wounded(self):
        self.state.on_wounded()

    def on_no_longer_wounded(self):
        self.state.on_no_longer_wounded()

    def set_state(self, state_class):
        old_state = self.state
        new_state = state_class(self)

        if old_state:
            old_state.on_state_exit(new_state)
            #old_state.brain = None

        self.state = new_state
        self.state.on_state_enter(old_state)


class KoboldState(object):
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

    def on_wounded(self):
        """Called when owner is critically wounded"""
        pass

    def on_no_longer_wounded(self):
        """Called when owner is no longer critically wounded"""
        pass

    def on_threat_lost(self, threat):
        """Called when a threatening entity is no longer in sight"""
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


class KoboldIdleState(KoboldState):
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
        self.brain.set_state(KoboldAggroState)

    def on_wounded(self):
        self.brain.set_state(KoboldHurtState)


class KoboldAggroState(KoboldState):
    """State class the encapsulates aggressive behavior"""
    def __init__(self, brain):
        super().__init__(brain)
        self.aggro_counter = 0
        self.aggro_cooldown = 5

    @property
    def threat(self):
        return self.brain.threat

    @threat.setter
    def threat(self, value):
        self.brain.threat = value

    def on_state_enter(self, prev_state):
        ani = animation.Flash('!', fg=palette.BRIGHT_YELLOW, bg=palette.BLACK)
        self.owner.append(ani)
        self.brain.add_action(action.IdleAction(self.owner))

    def on_state_exit(self, next_state):
        if isinstance(next_state, KoboldIdleState):
            ani = animation.Flash('?', fg=palette.BRIGHT_YELLOW, bg=palette.BLACK)
            self.owner.append(ani)
            self.brain.add_action(action.IdleAction(self.owner))

    def tick(self, tick):
        if self.threat:
            if self.aggro_counter <= 0:
                self.brain.add_action(movetoaction.MoveToAction(self.owner, self.threat.position, self.brain.owner.sight_radius))
                self.aggro_counter = self.aggro_cooldown

        else:
            self.brain.set_state(KoboldIdleState)

        self.aggro_counter -= 1

    def on_wounded(self):
        self.brain.fail_next_action()
        self.brain.actions = []
        self.brain.set_state(KoboldFleeState)


class KoboldHurtState(KoboldState):
    """Class that encapsulates hurt idle behavior"""
    def __init__(self, brain):
        super().__init__(brain)
        self.brain = brain

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
        """Called when a threatening entity is in sight"""
        self.brain.set_state(KoboldFleeState)

    def on_no_longer_wounded(self):
        self.brain.set_state(KoboldIdleState)


class KoboldFleeState(KoboldState):
    """Class that encapsulates hurt fleeing behavior"""
    def __init__(self, brain):
        super().__init__(brain)
        self.brain = brain

    @property
    def threat(self):
        return self.context.get('threat')

    @threat.setter
    def threat(self, value):
        self.context['threat'] = value

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
        self.brain.set_state(KoboldAggroState)

    def on_threat_lost(self, threat):
        self.brain.set_state(KoboldHurtState)
