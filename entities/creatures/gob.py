import random

import helpers
import instances
import palette
import registry
import utils

from ai import action
from ai.actions import moveaction
from ai.actions import movetoaction
from ai.actions import throwaction

from entities import animation
from entities import creature
from entities.items.weapons import fist
from entities.items.weapons import spear


class Gob(creature.Creature):
    def __init__(self, char='g', position=(0, 0), fg=palette.BRIGHT_GREEN, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)
        self.name = 'gob'
        self.max_health = 6
        self.current_health = self.max_health
        self.sight_radius = 4
        self.brain = creature.CreatureBrain(self)
        self.brain.set_state(GobIdleState)
        self.equip_weapon(spear.Spear())

registry.Registry.register(Gob, 'monster', 5)
registry.Registry.register(Gob, 'uncommon_monster', 5)


class GobIdleState(creature.CreatureIdleState):
    def on_threat_spotted(self, threat):
        # Forget whatever we were doing.
        self.brain.fail_next_action()
        self.brain.actions = []
        self.context['threat'] = threat
        self.brain.set_state(GobAggroState)

    def on_wounded(self):
        def on_wounded(self):
            self.brain.set_state(GobHurtState)

    def tick(self, tick):
        # Wait for our current plan to finish
        if self.brain.actions:
            return

        # Collect spear if we don't have one
        if not self.owner.weapon.isinstance('Spear'):
            s = [e for e in self.owner.visible_entities if e.isinstance('Spear')]
            if s:
                s = sorted(s, key=lambda t: utils.math.distance(self.owner.position, t.position))[0]
                act = movetoaction.MoveToAction(self.owner, s.position)
                self.brain.add_action(act)
                self.brain.add_action(action.IdleAction(self.owner))
                return

        # Wander
        if self.owner.visible_tiles:
            dest = random.choice(list(self.owner.visible_tiles))
            act = movetoaction.MoveToAction(self.owner, dest)
            self.brain.add_action(act)
            self.brain.add_action(action.IdleAction(self.owner))


class GobAggroState(creature.CreatureState):
    def __init__(self, brain):
        super().__init__(brain)
        self.aggro_counter = 0
        self.aggro_cooldown = 5
        self.current_target = self.get_nearest_threat()

    def on_state_enter(self, prev_state):
        ani = animation.Flash('!', fg=palette.BRIGHT_RED, bg=palette.BLACK)
        self.owner.append(ani)
        self.brain.add_action(action.IdleAction(self.owner))

    def on_state_exit(self, next_state):
        if isinstance(next_state, GobIdleState):
            ani = animation.Flash('?', fg=palette.BRIGHT_YELLOW, bg=palette.BLACK)
            self.owner.append(ani)
            self.brain.add_action(action.IdleAction(self.owner))

    def get_nearest_threat(self):
        threats = sorted([b for b in self.brain.threats if b.position], key=lambda t: utils.math.distance(self.owner.position, t.position))
        return threats[0] if threats else None

    def on_threat_lost(self, threat):
        if threat == self.current_target:
            self.current_target = self.get_nearest_threat()

        if not self.current_target:
            self.brain.set_state(GobIdleState)

    def on_wounded(self):
        self.brain.fail_next_action()
        self.brain.actions = []
        self.brain.set_state(GobFleeState)

    def tick(self, tick):
        if self.owner.weapon.isinstance('Spear'):
            # Are we lined up for a throw?
            if self.current_target.x == self.owner.x or self.current_target.y == self.owner.y:

                # Are we in range?
                dist = utils.math.distance(self.owner.position, self.current_target.position)
                if dist <= self.owner.weapon.throw_distance and dist > 1:
                    dir = utils.math.sub(self.current_target.position, self.owner.position)
                    dir = utils.math.normalize(dir)
                    dir = tuple(map(lambda i: int(i), dir))

                    s = self.owner.weapon
                    s.remove()
                    s.position = utils.math.add(self.owner.position, dir)
                    instances.scene_root.append(s)
                    self.owner.equip_weapon(fist.Fist())

                    act = throwaction.ThrowAction(self.owner, s)
                    self.brain.add_action(act)
                    self.brain.add_action(action.IdleAction(self.owner))
                    return

            # Attempt to line up a throw
            elif not self.brain.actions:
                dir = utils.math.sub(self.current_target.position, self.owner.position)

                if abs(dir[0]) < abs(dir[1]):
                    dir = dir[0], 0

                else:
                    dir = 0, dir[1]

                dir = utils.math.normalize(dir)
                dir = tuple(map(lambda i: int(i), dir))
                act = moveaction.MoveAction(self.owner, dir)
                self.brain.add_action(act)
                return

            # Attack enemy
            if self.aggro_counter <= 0:
                self.brain.add_action(movetoaction.MoveToAction(self.owner, self.current_target.position, self.brain.owner.sight_radius))
                self.aggro_counter = self.aggro_cooldown

            self.aggro_counter -= 1
            return

        # Go get our spear
        elif not self.brain.actions:
            s = [e for e in self.owner.visible_entities if e.isinstance('Spear')]
            if s:
                s = sorted(s, key=lambda t: utils.math.distance(self.owner.position, t.position))[0]
                act = movetoaction.MoveToAction(self.owner, s.position)
                self.brain.add_action(act)
                self.brain.add_action(action.IdleAction(self.owner))
                return

        # Attack enemy
        if self.aggro_counter <= 0:
            self.brain.add_action(movetoaction.MoveToAction(self.owner, self.current_target.position, self.brain.owner.sight_radius))
            self.aggro_counter = self.aggro_cooldown

        self.aggro_counter -= 1


class GobHurtState(creature.CreatureState):
    def on_no_longer_wounded(self):
        self.brain.set_state(GobIdleState)

    def on_threat_spotted(self, threat):
        """Called when a threatening entity is in sight"""
        if threat.current_health > self.owner.weapon.damage:
            self.brain.set_state(GobFleeState)

    def tick(self, tick):
        if self.brain.actions:
            return

        # Attempt to heal
        potions = [e for e in self.owner.visible_entities if e.isinstance('Potion') and e.position != self.owner.position]
        potions = sorted(potions, key=lambda c: utils.math.distance(self.owner.position, c.position))

        if potions:
            act = movetoaction.MoveToAction(self.owner, potions[0].position)
            self.brain.add_action(act)
            return

        # Collect spear if we don't have one
        if not self.owner.weapon.isinstance('Spear'):
            s = [e for e in self.owner.visible_entities if e.isinstance('Spear')]
            if s:
                s = sorted(s, key=lambda t: utils.math.distance(self.owner.position, t.position))[0]
                act = movetoaction.MoveToAction(self.owner, s.position)
                self.brain.add_action(act)
                self.brain.add_action(action.IdleAction(self.owner))
                return

        # Wander
        if self.owner.visible_tiles:
            dest = random.choice(list(self.owner.visible_tiles))
            act = movetoaction.MoveToAction(self.owner, dest)
            self.brain.add_action(act)
            self.brain.add_action(action.IdleAction(self.owner))


class GobFleeState(creature.CreatureState):
    """Class that encapsulates hurt fleeing behavior"""
    def __init__(self, brain):
        super().__init__(brain)
        self.brain = brain
        self.current_target = self.get_nearest_threat()

    def get_nearest_threat(self):
        threats = sorted([b for b in self.brain.threats if b.position], key=lambda t: utils.math.distance(self.owner.position, t.position))
        return threats[0] if threats else None

    def on_no_longer_wounded(self):
        self.brain.set_state(GobAggroState)

    def on_threat_lost(self, threat):
        if threat == self.current_target:
            self.current_target = self.get_nearest_threat()

        if self.current_target:
            self.brain.set_state(GobFleeState)

        else:
            self.brain.set_state(GobHurtState)

    def tick(self, tick):
        # Neighboring tiles
        possible_tiles = [utils.math.add(self.owner.position, d) for d in helpers.DirectionHelper.directions]

        # Possible tiles
        possible_tiles = [d for d in possible_tiles if instances.scene_root.check_collision(*d)]

        # Determine furthest tiles
        possible_tiles = sorted(possible_tiles, key=lambda x: utils.math.distance(x, self.current_target.position), reverse=True)

        direction = utils.math.sub(possible_tiles[0], self.owner.position)

        act = moveaction.MoveAction(self.owner, direction)
        self.brain.add_action(act)
