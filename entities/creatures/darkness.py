import instances
import palette
import utils

from ai import action
from ai import brain
from ai.actions import movetoaction

from entities.creatures import monster
from entities.items.weapons import fist


class Darkness(monster.Monster):
    def __init__(self, position=(0,0)):
        super().__init__(' ', position, fg=palette.MAGENTA, bg=palette.BLACK)
        self.name = ''
        self.brain = DarknessBrain(self)
        self.equip_weapon(TouchOfDarkness())

    def on_attacked(self, action):
        pass

    def allow_throw(self, action):
        return False


class TouchOfDarkness(fist.Fist):
    def __init__(self, char=' ', position=(0, 0)):
        super().__init__(char, position)
        self.name = ''
        self.verb = ''

    def get_special_action(self, requester, target):
        if target.isinstance('Creature') and not target.isinstance('Darkness'):
            return TurnToDark(requester, target)


class TurnToDark(action.Action):
    def perform(self):
        self.target.die()
        self.performer.brain.add_action(action.IdleAction(self.performer))
        d = Darkness(position=self.performer.position)
        instances.scene_root.append(d)


class DarknessBrain(brain.Brain):
    def __init__(self, owner):
        super().__init__(owner)
        self.state = DarknessAggroState(self)

    def tick(self, tick):
        self.state.tick(tick)


class DarknessAggroState(monster.MonsterAggroState):
    def __init__(self, brain):
        self.brain = brain

    def tick(self, tick):
        pf = instances.scene_root.level.darkness_pathfinder

        entities = [e for e in instances.scene_root.children if e.isinstance('Creature') and not e.isinstance('Darkness') and pf.get_path(*self.owner.position, *e.position)]

        if not entities:
            return

        nearest_entity = sorted(entities, key=lambda t: utils.math.distance(self.owner.position, t.position))[0]

        act = movetoaction.MoveToAction(self.owner, nearest_entity.position, 1)
        self.owner.brain.add_action(act)
        self.owner.brain.perform_action()
