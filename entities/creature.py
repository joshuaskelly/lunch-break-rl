import random

import tdl

import helpers
import instances
import palette
import utils

from ai import action
from ai import brain
from ai.actions import attackaction
from ai.actions import wanderaction
from ai.actions import moveaction
from ai.actions import movetoaction

from entities import animation
from entities import entity
from entities.items.consumables import corpse
from entities.items.weapons import debris
from entities.items.weapons import fist


class Creature(entity.Entity):
    def __init__(self, char, position=(0, 0), fg=palette.BRIGHT_WHITE, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)
        self.brain = brain.Brain(self)
        self.statuses = []
        self.name = 'Creature'
        self.current_health = 10
        self.max_health = 10
        self.weapon = None
        self.visible_tiles = set()
        self.sight_radius = 7.5

        self.equip_weapon(fist.Fist())

    @property
    def alive(self):
        return self.current_health > 0

    def move(self, x, y):
        dest = self.position[0] + x, self.position[1] + y

        action_to_perform = None
        target_entity = None

        for target_entity in instances.scene_root.get_entity_at(*dest):
            # Get bumped entity's default action
            action_to_perform = self.weapon.get_special_action(self, target_entity)

            if not action_to_perform:
                action_to_perform = target_entity.get_action(self)

            if action_to_perform:
                break

        # Perform the action if possible
        if action_to_perform and action_to_perform.prerequisite():
            action_to_perform.perform()

            # Because we have bumped, cancel our move action
            next_action = self.brain.actions[0] if self.brain.actions else None
            if next_action and \
                not action_to_perform.isinstance('SwapPositionAction') and \
                next_action.isinstance('MoveAction') and \
                next_action.parent:

                next_action.fail()

        if target_entity and target_entity.position == dest and action_to_perform:
            return

        if self.can_move(x, y):
            self.position = self.position[0] + x, self.position[1] + y

    def can_move(self, x, y):
        if not self.position:
            return False

        dest = self.position[0] + x, self.position[1] + y
        return dest in instances.scene_root.level.data

    def can_see(self, target):
        """Returns true if target entity is in sight"""
        if not target or not target.position:
            return False

        return target.position in self.visible_tiles

    def update(self, time):
        super().update(time)
        for status in self.statuses:
            status.update(time)

    def update_fov(self):
        if not self.position:
            return

        x, y = self.position
        self.visible_tiles = tdl.map.quick_fov(x, y, lambda x, y: not instances.scene_root.is_visibility_blocked(x, y), radius=self.sight_radius)

    def equip_weapon(self, new_item):
        self.weapon = new_item
        self.weapon.hidden = True
        self.append(new_item)

    def drop_weapon(self):
        if not self.weapon.isinstance('Fist'):
            i = self.weapon
            i.remove()
            i.hidden = False
            i.position = self.position
            instances.scene_root.append(i)
            self.equip_weapon(fist.Fist())
            instances.console.describe(self, '{} drops {}'.format(self.display_string, i.display_string), 'Something clatters to the ground')

    def break_weapon(self):
        if not self.weapon.isinstance('Fist'):
            i = self.weapon
            i.remove()
            self.equip_weapon(debris.Debris())
            instances.console.describe(self, '{}\'s {} breaks!'.format(self.display_string, i.display_string))

    def die(self):
        if self.current_health > 0:
            self.current_health = 0

        c = corpse.Corpse(self)
        c.position = self.position
        instances.scene_root.append(c)

        self.drop_weapon()
        instances.console.describe(self, '{} perishes!'.format(self.display_string), 'Something cries its last')
        self.remove()

    def make_blood_trail(self):
        level_entity = instances.scene_root.get_level_entity_at(*self.position)
        level_entity.fg = palette.BRIGHT_RED

    def remove(self, child=None):
        super().remove(child)

        if not child:
            self.brain.clear()

    def tick(self, tick):
        super().tick(tick)

        for status in self.statuses:
            status.tick(tick)

        self.brain.tick(tick)
        self.brain.perform_action()
        self.update_fov()

        if not self.alive:
            self.die()

        if self.current_health == 1 and self.max_health > 1:
            self.make_blood_trail()

    def handle_events(self, event):
        super().handle_events(event)
        self.brain.handle_events(event)

    def get_action(self, requester=None):
        direction = utils.math.sub(self.position, requester.position)
        return attackaction.AttackAction(requester, self, direction)

    @property
    def visible_entities(self):
        current_scene = instances.scene_root
        result = []

        for e in current_scene.children:
            if not e.isinstance('Entity'):
                continue

            if e == self:
                continue

            if e.position in self.visible_tiles:
                result.append(e)

        return result

    def add_status(self, status):
        # Check and handle duplicate statuses
        duplicate_status = [s for s in self.statuses if status.__class__ == s.__class__]
        if duplicate_status:
            duplicate = duplicate_status[0]
            duplicate.stack(status)

        # Otherwise apply status
        else:
            status.on_status_begin()
            self.statuses.append(status)

    def remove_status(self, status):
        status.on_status_end()
        self.statuses.remove(status)

    def can_attack(self, target):
        """Determines if performer can attack target
        
        target: An entity
        """
        return self.weapon.state.can_attack(target)

    def allow_attack(self, action):
        """Determines if target will allow attack"""
        return self.weapon.state.allow_attack(action)

    def before_attacked(self, action):
        """Called on target before attack occurs"""
        self.weapon.state.before_attacked(action)

    def on_attacked(self, action):
        """Called on target to handle being attacked"""
        self.weapon.state.on_attacked(action)

        damage_dealt = action.performer.weapon.damage
        verb = action.performer.weapon.verb

        instances.console.describe(action.performer, '{} {} {}'.format(action.performer.display_string, verb, action.target.display_string))

        self.current_health -= damage_dealt

        if damage_dealt > 0:
            ani = animation.FlashBackground(bg=palette.BRIGHT_RED)
            self.append(ani)

            self.make_blood_trail()

        if not self.alive:
            self.die()

    def after_attacked(self, action):
        """Called on target after attack has occurred"""
        self.weapon.state.after_attacked(action)

    def before_attack(self, action):
        """Called on performer before attack occurs"""
        self.weapon.state.before_attack(action)

    def after_attack(self, action):
        """Called on performer after attack has occurred"""
        self.weapon.state.after_attack(action)


class CreatureBrain(brain.Brain):
    def __init__(self, owner):
        super().__init__(owner)
        self.state = None
        self.context = {'threats': []}
        self.set_state(CreatureIdleState)
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
        if self.last_health > self.owner.current_health:
            # We are hurt bad
            if self.last_health > self.wounded_threshold >= self.owner.current_health:
                self.on_wounded()

            else:
                self.on_hurt()

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

    def on_hurt(self):
        self.state.on_hurt()

    def on_wounded(self):
        self.state.on_wounded()

    def on_no_longer_wounded(self):
        self.state.on_no_longer_wounded()

    def reset(self):
        self.clear()
        self.set_state(CreatureIdleState)


class CreatureState(object):
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

    def handle_events(self, event):
        pass

    def on_threat_spotted(self, threat):
        """Called when a threatening entity is in sight"""
        pass

    def on_threat_lost(self, threat):
        """Called when a threatening entity is no longer in sight"""
        pass

    def on_hurt(self):
        """Called when owner is hurt"""
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


class CreatureIdleState(CreatureState):
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
        self.brain.set_state(CreatureAggroState)

    def on_wounded(self):
        self.brain.set_state(CreatureHurtState)


class CreatureAggroState(CreatureState):
    """State class the encapsulates aggressive behavior"""

    def __init__(self, brain):
        super().__init__(brain)
        self.aggro_counter = 0
        self.aggro_cooldown = 5
        self.current_target = self.get_nearest_threat()

    def get_nearest_threat(self):
        threats = sorted([b for b in self.brain.threats if b.position], key=lambda t: utils.math.distance(self.owner.position, t.position))
        return threats[0] if threats else None

    def on_state_enter(self, prev_state):
        ani = animation.Flash('!', fg=palette.BRIGHT_RED, bg=palette.BLACK)
        self.owner.append(ani)
        self.brain.add_action(action.IdleAction(self.owner))

    def on_state_exit(self, next_state):
        if isinstance(next_state, CreatureIdleState):
            ani = animation.Flash('?', fg=palette.BRIGHT_YELLOW, bg=palette.BLACK)
            self.owner.append(ani)
            self.brain.add_action(action.IdleAction(self.owner))

    def tick(self, tick):
        if self.aggro_counter <= 0:
            self.brain.add_action(movetoaction.MoveToAction(self.owner, self.current_target.position, self.brain.owner.sight_radius))
            self.aggro_counter = self.aggro_cooldown

        self.aggro_counter -= 1

    def on_threat_lost(self, threat):
        if threat == self.current_target:
            self.current_target = self.get_nearest_threat()

        if not self.current_target:
            self.brain.set_state(CreatureIdleState)

    def on_wounded(self):
        self.brain.fail_next_action()
        self.brain.actions = []
        self.brain.set_state(CreatureFleeState)


class CreatureHurtState(CreatureState):
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
        self.brain.set_state(CreatureFleeState)

    def on_no_longer_wounded(self):
        self.brain.set_state(CreatureIdleState)


class CreatureFleeState(CreatureState):
    """Class that encapsulates hurt fleeing behavior"""

    def __init__(self, brain):
        super().__init__(brain)
        self.brain = brain
        self.current_target = self.get_nearest_threat()

    def get_nearest_threat(self):
        threats = sorted([b for b in self.brain.threats if b.position], key=lambda t: utils.math.distance(self.owner.position, t.position))
        return threats[0] if threats else None

    def tick(self, tick):
        if self.current_target and self.current_target.position:
            # Neighboring tiles
            possible_tiles = [utils.math.add(self.owner.position, d) for d in helpers.DirectionHelper.directions]

            # Possible tiles
            possible_tiles = [d for d in possible_tiles if instances.scene_root.check_collision(*d)]

            # Determine furthest tiles
            possible_tiles = sorted(possible_tiles, key=lambda x: utils.math.distance(x, self.current_target.position), reverse=True)

            direction = utils.math.sub(possible_tiles[0], self.owner.position)

            act = moveaction.MoveAction(self.owner, direction)
            self.brain.add_action(act)

    def on_no_longer_wounded(self):
        self.brain.set_state(CreatureAggroState)

    def on_threat_lost(self, threat):
        if threat == self.current_target:
            self.current_target = self.get_nearest_threat()

        if not self.current_target:
            self.brain.set_state(CreatureHurtState)

    def on_state_enter(self, prev_state):
        ani = animation.Flash('!', fg=palette.BRIGHT_BLUE, bg=palette.BLACK)
        self.owner.append(ani)
        self.brain.add_action(action.IdleAction(self.owner))

    def on_state_exit(self, next_state):
        if isinstance(next_state, CreatureHurtState):
            ani = animation.Flash('?', fg=palette.BRIGHT_YELLOW, bg=palette.BLACK)
            self.owner.append(ani)
            self.brain.add_action(action.IdleAction(self.owner))


class CreatureSleepState(CreatureState):
    def __init__(self, brain):
        super().__init__(brain)
        self.old_sight_radius = self.owner.sight_radius
        self.sleep_animation = None
        self._sleep_timer = 0
        self.sleep_timer = random.randrange(10, 45)

    @property
    def sleep_timer(self):
        return self._sleep_timer

    @sleep_timer.setter
    def sleep_timer(self, value):
        value = int(value)
        self._sleep_timer = value

        if self.sleep_animation:
            self.sleep_animation.remove()

        self.sleep_animation = animation.Flash('Z', fg=palette.BRIGHT_BLUE, bg=palette.BLACK, interval=0.5, repeat=value * 4)
        self.owner.append(self.sleep_animation)

    def tick(self, tick):
        self.sleep_timer -= 1
        if self.sleep_timer <= 0 and random.random() < 1 / 8:
            self.wakeup()

    def on_state_enter(self, prev_state):
        self.owner.sight_radius = 0.5
        self.brain.clear()
        instances.console.describe(self.owner, '{} fell asleep!'.format(self.owner.display_string))

    def on_hurt(self):
        self.wakeup()

    def on_state_exit(self, next_state):
        self.owner.sight_radius = self.old_sight_radius
        self.owner.remove(self.sleep_animation)

    def wakeup(self):
        self.owner.sight_radius = self.old_sight_radius
        self.owner.remove(self.sleep_animation)
        self.brain.reset()
        instances.console.describe(self.owner, '{} wakes up!'.format(self.owner.display_string))