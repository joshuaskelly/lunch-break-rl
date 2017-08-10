import utils

from ai import action


class DirectionHelper(object):
    valid_moves = 'u', 'd', 'l', 'r', 'U', 'D', 'L', 'R'
    dir_map = {
        (1, 0): 'R',
        (0, 1): 'D',
        (-1, 0): 'L',
        (0, -1): 'U',
        'R': (1, 0),
        'D': (0, 1),
        'L': (-1, 0),
        'U': (0, -1),
        'r': (1, 0),
        'd': (0, 1),
        'l': (-1, 0),
        'u': (0, -1)
    }

    @staticmethod
    def get_direction(direction):
        return DirectionHelper.dir_map.get(direction)


class MoveHelper(object):
    @staticmethod
    def path_to_moves(start, path):
        # Calculate relative deltas
        a = path[:]
        b = path[:-1]
        b.insert(0, start)
        z = list(zip(a, b))

        def func(item):
            lhs = item[0]
            rhs = item[1]

            return utils.math.sub(lhs, rhs)

        deltas = list(map(func, z))

        # Convert deltas to moves
        moves = [DirectionHelper.get_direction(i) for i in deltas]

        return moves

    @staticmethod
    def move_to_action(move):
        if move in DirectionHelper.dir_map:
            return action.MoveAction(DirectionHelper.get_direction(move.upper()))

        return None
