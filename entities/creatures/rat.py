import random

import helpers
import instances
import palette
import utils
import registry

from ai import action
from ai import brain
from ai.actions import moveaction
from ai.actions import movetoaction
from ai.actions import wanderaction
from ai.actions import swappositionaction

from entities import animation
from entities import entity
from entities.creatures import monster
from entities.items.weapons import fist


class Rat(monster.Monster):
    def __init__(self, char='r', position=(0, 0)):
        super().__init__(char, position)
        self.name = 'rat'
        self.brain = RatBrain(self)
        self.max_health = 1
        self.current_health = self.max_health
        self.sight_radius = 2.5
        self.equip_weapon(RatTeeth())

    def can_equip(self, target):
        return target.isinstance('Fist')

    def get_action(self, requester=None):
        # Rats won't hurt other rats. :)
        if requester.isinstance('Rat'):
            if (requester.isinstance('RatKing') or self.isinstance('RatKing') or random.random() < 1 / 96):
                return CreateRatKingAction(requester, self)

            return swappositionaction.SwapPositionAction(requester, self)

        return super().get_action(requester)

registry.Registry.register(Rat, 'monster', 3)


class RatTeeth(fist.Fist):
    def __init__(self, char='f', position=(0, 0)):
        super().__init__(char, position)
        self.name = 'teeth'
        self.verb = 'bites'

    def get_special_action(self, requester, target):
        # TODO: Makes the below actions
        if target.isinstance('Corpse') or target.isinstance('Creature') and hasattr(target.brain, 'state') and isinstance(target.brain.state, monster.MonsterSleepState):
            # Add babies
            return InfestAction(requester, target)

        elif target.isinstance('Weapon'):
            # Nibble
            if target.isinstance('Debris') or random.random() <= 0.5:
                return None

            else:
                return NibbleWeaponAction(requester, target)

        return None


class InfestAction(action.Action):
    def prerequisite(self):
        return utils.math.distance(self.performer.position, self.target.position) == 1

    def perform(self):
        rbs = [b for b in self.target.children if b.isinstance('RatBabies')]

        if not rbs:
            self.target.append(RatBabies())


class NibbleWeaponAction(action.Action):
    def prerequisite(self):
        return utils.math.distance(self.performer.position, self.target.position) == 1 and self.target.isinstance('Weapon')

    def perform(self):
        instances.console.describe(self.performer, "{} nibbles on {}".format(self.performer.display_string, self.target.display_string))

        for _ in range(self.performer.weapon.damage):
            if self.target.parent:
                self.target.on_use()


class CreateRatKingAction(action.Action):
    def prerequisite(self):
        return utils.math.distance(self.performer.position, self.target.position) == 1 and self.target.isinstance('Rat')

    def perform(self):
        a = self.performer
        b = self.target

        health = sum([e.max_health for e in [a, b]])
        rk = RatKing(position=b.position, health=health)

        if not a.isinstance('RatKing') and not b.isinstance('RatKing'):
            instances.console.describe(rk, 'A {} forms!'.format(rk.display_string))

        a.remove()
        b.remove()

        instances.scene_root.append(rk)


class RatBrain(brain.Brain):
    def __init__(self, owner):
        super().__init__(owner)
        self.state = None
        self.context = {'threats': [],
                        'allies': []}
        self.set_state(RatIdleState)
        self.last_health = owner.current_health

    @property
    def threats(self):
        return self.context.get('threats')

    @threats.setter
    def threats(self, value):
        self.context['threats'] = value

    @property
    def allies(self):
        return self.context.get('allies')

    @allies.setter
    def allies(self, value):
        self.context['allies'] = value

    def tick(self, tick):
        if not self.owner.alive:
            return

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

        self.allies = [e for e in self.owner.visible_entities if e.isinstance('Rat') and e.position and e.alive]

        self.state.tick(tick)

    def get_threats(self):
        return [e for e in self.owner.visible_entities if self.is_threat(e)]

    def is_threat(self, entity):
        if entity.isinstance('Creature') and entity.alive:
            if entity.isinstance('Rat') or entity.isinstance('Darkness'):
                return False

            elif hasattr(entity.brain, 'state') and isinstance(entity.brain.state, monster.MonsterSleepState):
                return False

            elif entity.current_health >= self.owner.current_health:
                return True

        return False

    def set_state(self, state_class):
        if not self.owner.alive:
            return

        old_state = self.state
        new_state = state_class(self)

        if old_state:
            old_state.on_state_exit(new_state)

        self.state = new_state
        self.state.on_state_enter(old_state)


class RatIdleState(monster.MonsterState):
    """State class that encapsulates idle behavior"""

    def __init__(self, brain):
        super().__init__(brain)

    def tick(self, tick):
        if not self.brain.actions:
            # Lay babies...
            if random.random() < 1 / 32:
                corpses = [e for e in self.owner.visible_entities if (e.isinstance('Corpse') or e.isinstance('Creature') and hasattr(e.brain, 'state') and isinstance(e.brain.state, monster.MonsterSleepState)) and e.position != self.owner.position]
                corpses = sorted(corpses, key=lambda c: utils.math.distance(self.owner.position, c.position))

                target = corpses[0] if corpses else None

                if target:
                    act = movetoaction.MoveToAction(self.owner, target.position)
                    self.brain.add_action(act)

            # ...or wander.
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
        allies = self.brain.allies[:]
        allies.append(self.owner)
        health = sum([a.current_health for a in allies])

        if health > threat.current_health:
            for ally in allies:
                ally.brain.set_state(RatAggroState)
                ally.brain.state.threat = threat

        else:
            # Forget whatever we were doing.
            self.brain.fail_next_action()
            self.brain.actions = []
            self.context['threat'] = threat
            self.brain.set_state(RatFleeState)


class RatAggroState(monster.MonsterState):
    """State class the encapsulates aggressive behavior"""

    def __init__(self, brain):
        super().__init__(brain)
        self.aggro_counter = 0
        self.aggro_cooldown = 5
        self.threat_visible = True
        self.threat_lost_counter = 0

        threats = sorted(self.brain.threats, key=lambda t: utils.math.distance(self.owner.position, t.position))
        self.threat = threats[0] if threats else None

        if not self.threat:
            self.threat_visible = False

    def on_state_enter(self, prev_state):
        ani = animation.Flash('!', fg=palette.BRIGHT_RED, bg=palette.BLACK)
        self.owner.append(ani)
        self.brain.add_action(action.IdleAction(self.owner))

    def on_state_exit(self, next_state):
        if isinstance(next_state, RatIdleState):
            ani = animation.Flash('?', fg=palette.BRIGHT_YELLOW, bg=palette.BLACK)
            self.owner.append(ani)
            self.brain.add_action(action.IdleAction(self.owner))

    def tick(self, tick):
        if self.aggro_counter <= 0 and self.threat_lost_counter == 0:
            self.brain.add_action(movetoaction.MoveToAction(self.owner, self.threat.position, self.brain.owner.sight_radius))
            self.aggro_counter = self.aggro_cooldown

        self.aggro_counter -= 1

        if not self.threat_visible:
            self.threat_lost_counter += 1

            if self.threat_lost_counter >= 5:
                self.threat = None
                self.brain.set_state(RatIdleState)

        allies = self.brain.allies[:]
        allies.append(self.owner)
        health = sum([a.current_health for a in allies])

    def on_threat_spotted(self, threat):
        if threat == self.threat:
            self.threat_visible = True

    def on_threat_lost(self, threat):
        if threat == self.threat:
            self.threat_visible = False


class RatFleeState(monster.MonsterState):
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

    def on_threat_lost(self, threat):
        if threat == self.threat:
            self.threat = None
            self.brain.set_state(RatIdleState)

    def on_state_enter(self, prev_state):
        ani = animation.Flash('!', fg=palette.BRIGHT_BLUE, bg=palette.BLACK)
        self.owner.append(ani)
        self.brain.add_action(action.IdleAction(self.owner))

    def on_state_exit(self, next_state):
        if isinstance(next_state, RatIdleState):
            ani = animation.Flash('?', fg=palette.BRIGHT_YELLOW, bg=palette.BLACK)
            self.owner.append(ani)
            self.brain.add_action(action.IdleAction(self.owner))


class RatBabies(entity.Entity):
    def __init__(self):
        super().__init__('R')
        self.timer = 30
        self.hidden = True

    def tick(self, tick):
        self.timer -= 1

        if self.timer == 5 and self.parent.isinstance('Creature'):
            instances.console.describe(self.parent, '{} looks ill'.format(self.parent.display_string))

        if self.timer == 0:
            parent = self.parent

            if not parent.position:
                return

            neighbor_tiles = list(map(lambda x: utils.math.add(x, parent.position), helpers.DirectionHelper.directions))
            open_tiles = [t for t in neighbor_tiles if instances.scene_root.check_collision(*t)]

            if open_tiles:
                instances.console.describe(parent, 'Rats burst from {}'.format(parent.display_string))

            if parent.isinstance('Creature'):
                parent.die()
            else:
                parent.remove()

            for tile in open_tiles:
                r = Rat(position=tile)
                instances.scene_root.append(r)


class RatKing(Rat):
    def __init__(self, char='R', position=(0, 0), health=2):
        super().__init__(char, position)
        self.name = 'rat king'
        self.current_health = health
        self.max_health = health
        self.weapon.damage = health

    def on_attacked(self, action):
        a = self.max_health // 2
        b = self.max_health - a

        instances.console.describe(self, '{} splits in two!'.format(self.display_string))

        pos = self.position
        self.remove()

        neighbor_tiles = list(map(lambda x: utils.math.add(x, pos), helpers.DirectionHelper.directions))
        neighbor_tiles.append(pos)
        open_tiles = [t for t in neighbor_tiles if instances.scene_root.check_collision(*t)]
        empty_tiles = [t for t in open_tiles if not instances.scene_root.get_entity_at(*t)]

        a_pos = empty_tiles.pop(int(random.random() * (len(empty_tiles) - 1)))

        b_pos = a_pos
        if empty_tiles:
            b_pos = empty_tiles.pop(int(random.random() * (len(empty_tiles) - 1)))

        if a == 1:
            instances.scene_root.append(Rat(position=a_pos))
        else:
            instances.scene_root.append(RatKing(position=a_pos, health=a))

        if b == 1:
            instances.scene_root.append(Rat(position=b_pos))
        else:
            instances.scene_root.append(RatKing(position=b_pos, health=b))
