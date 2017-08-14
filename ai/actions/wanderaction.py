import random

from ai import action
from ai.actions import moveaction


class WanderAction(action.Action):
    def prerequisite(self):
        return True

    def perform(self):
        moves = (1, 0), (-1, 0), (0, 1), (0, -1)

        number_of_moves = random.randint(1, 3)
        batched_move = action.BatchedAction(self.performer)

        for _ in range(number_of_moves):
            move_action = moveaction.MoveAction(self.performer, moves[random.randint(0, 3)])
            move_action.parent = batched_move
            self.performer.brain.add_action(move_action)

        self.performer.brain.add_action(batched_move)
