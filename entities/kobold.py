import random

import instances
import palette
import registry

from ai import action
from ai import brain
from entities import animation
from entities import creature
from entities import item


class Kobold(creature.Creature):
    def __init__(self, char='K', position=(0, 0), fg=palette.BRIGHT_GREEN, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg=(0, 0, 0))
        self.name = 'kobold'
        self.brain = KoboldBrain(self)
        self.max_health = 4
        self.current_health = self.max_health
        self.sight_radius = 3.5

        if random.randint(0, 3) == 0:
            self.held_item = item.Sword()

registry.Registry.register(Kobold, 'monster', 'common')


class KoboldBrain(brain.Brain):
    def __init__(self, owner):
        super().__init__(owner)
        self.player_aggro = 0
        self.is_aggro = False

    def can_see_player(self):
        return len([e for e in self.owner.visible_entities if e.__class__.__name__ == 'Player'])

    def perform_action(self):
        if self.can_see_player() and self.player_aggro <= 0:
            self.player_aggro = 5
            self.fail_next_action()
            # instances.console.print('Can see player!')

            if not self.is_aggro:
                ani = animation.Flash('!', fg=palette.BRIGHT_YELLOW, bg=palette.BLACK)
                self.owner.append(ani)
                self.is_aggro = True

            player = [e for e in self.owner.visible_entities if e.__class__.__name__ == 'Player'][0]
            self.add_action(action.IdleAction())
            self.add_action(action.MoveToAction(player.position, self.owner.sight_radius))

        else:
            self.player_aggro -= 1

            if self.is_aggro:
                ani = animation.Flash('?', fg=palette.BRIGHT_YELLOW, bg=palette.BLACK)
                self.owner.append(ani)
                self.add_action(action.IdleAction())
                self.is_aggro = False

            # Idle behavior. Wait and wander.
            if not self.actions:
                batched_action = action.BatchedMoveAction()

                for _ in range(random.randint(1, 3)):
                    idle_action = action.IdleAction()
                    idle_action.parent = batched_action
                    self.add_action(idle_action)

                wander_action = action.WanderAction()
                wander_action.parent = batched_action
                self.add_action(wander_action)

                self.add_action(batched_action)

        super().perform_action()


