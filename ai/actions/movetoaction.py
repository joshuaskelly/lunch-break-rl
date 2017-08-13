import helpers
import instances

from ai import action


class MoveToAction(action.Action):
    def __init__(self, destination, max_moves=None):
        super().__init__()
        self.destination = destination
        self.max_moves = int(max_moves)

    def prerequisite(self, owner):
        scene_root = instances.scene_root
        level = scene_root.level

        return self.destination in level.data and scene_root.check_collision(*self.destination)

    def perform(self, owner):
        path = instances.scene_root.level.pathfinder.get_path(*owner.position, *self.destination)

        if self.max_moves:
            path = path[:self.max_moves]

        moves = helpers.MoveHelper.path_to_moves(owner.position, path)

        if not moves:
            return

        batched_move = action.BatchedAction()
        first_move = None

        for command in moves:
            move_action = helpers.MoveHelper.move_to_action(command)

            if move_action:
                move_action.parent = batched_move
                owner.brain.add_action(move_action)

                if not first_move:
                    first_move = move_action

        owner.brain.add_action(batched_move)

        if owner.brain.actions[0] is first_move:
            owner.brain.perform_action()
