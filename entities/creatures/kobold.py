import random

import palette
import registry

from ai import action
from ai import brain

from ai.actions import wanderaction
from ai.actions import movetoaction

from entities import animation
from entities import creature

from entities.items.weapons import dagger


class Kobold(creature.Creature):
    def __init__(self, char='K', position=(0, 0), fg=palette.BRIGHT_GREEN, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)
        self.name = 'kobold'
        self.brain = KoboldBrain(self)
        self.max_health = 4
        self.current_health = self.max_health
        self.sight_radius = 3.5

        if random.random() <= 1 / 5:
            self.equip_weapon(dagger.Dagger())

registry.Registry.register(Kobold, 'monster', 'common')


class KoboldBrain(brain.Brain):
    def __init__(self, owner):
        super().__init__(owner)
        self.state = None
        self.context = {}
        self.set_state(KoboldIdleState)

    def tick(self, tick):
        self.state.tick(tick)

    def get_nearest_threat(self):
        """Returns the closes visible entity that is a threat"""
        threats = [e for e in self.owner.visible_entities if self.is_threat(e)]
        if threats:
            return threats[0]

        return None

    def is_threat(self, entity):
        return entity.isinstance('Player')

    def set_state(self, state_class):
        old_state = self.state
        new_state = state_class(self)

        if old_state:
            old_state.on_state_exit(new_state)
            old_state.brain = None

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

    def on_threat_spotted(self, player):
        """Called when a threatening entity is in sight"""
        pass

    def on_threat_lost(self, player):
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
        threat = self.brain.get_nearest_threat()
        if threat:
            # Forget whatever we were doing.
            self.brain.fail_next_action()
            self.brain.actions = []
            self.context['threat'] = threat
            self.brain.set_state(KoboldAggroState)

        else:
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

    def on_threat_spotted(self, player):
        self.brain.set_state(KoboldAggroState)


class KoboldAggroState(KoboldState):
    """State class the encapsulates aggressive behavior"""
    def __init__(self, brain):
        super().__init__(brain)
        self.aggro_counter = 0
        self.aggro_cooldown = 5

    @property
    def threat(self):
        return self.context.get('threat')

    def on_state_enter(self, prev_state):
        ani = animation.Flash('!', fg=palette.BRIGHT_YELLOW, bg=palette.BLACK)
        self.owner.append(ani)
        self.brain.add_action(action.IdleAction(self.owner))

    def on_state_exit(self, next_state):
        ani = animation.Flash('?', fg=palette.BRIGHT_YELLOW, bg=palette.BLACK)
        self.owner.append(ani)
        self.brain.add_action(action.IdleAction(self.owner))
        self.context['threat'] = None

    def tick(self, tick):
        if self.owner.can_see(self.threat):
            if self.aggro_counter <= 0:
                self.brain.add_action(movetoaction.MoveToAction(self.owner, self.threat.position, self.brain.owner.sight_radius))
                self.aggro_counter = self.aggro_cooldown

        else:
            self.brain.set_state(KoboldIdleState)

        self.aggro_counter -= 1
