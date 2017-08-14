import helpers
import instances

from ai import action


class MoveToAction(action.Action):
    def __init__(self, performer, destination, max_moves=None):
        super().__init__(performer)
        self.destination = destination
        self.max_moves = int(max_moves)

    def prerequisite(self):
        scene_root = instances.scene_root
        level = scene_root.level

        return self.destination in level.data and scene_root.check_collision(*self.destination)

    def perform(self):
        path = instances.scene_root.level.pathfinder.get_path(*self.performer.position, *self.destination)

        if self.max_moves:
            path = path[:self.max_moves]

        moves = helpers.MoveHelper.path_to_moves(self.performer.position, path)

        if not moves:
            return

        batched_move = action.BatchedAction(self.performer)
        first_move = None

        for command in moves:
            move_action = helpers.MoveHelper.move_to_action(self.performer, command)

            if move_action:
                move_action.parent = batched_move
                self.performer.brain.add_action(move_action)

                if not first_move:
                    first_move = move_action

        self.performer.brain.add_action(batched_move)

        if self.performer.brain.actions[0] is first_move:
            self.performer.brain.perform_action()
