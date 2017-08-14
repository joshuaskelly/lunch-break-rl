from math import sqrt

def cp437(string):
    """Converts utf8 to codepage 437"""
    return ''.join([chr(ord(c.encode('cp437'))) for c in string])


def rect(x, y, width, height):
    result = []

    for i in range(width):
        for j in range(height):
            result.append((i + x, j + y))

    return result


def is_next_to(e1, e2):
    """Returns true if the given entities are positioned next to each other.

    e1: An entity

    e2: An entity

    Returns True if they are orthogonally adjacent
    """
    if not e1 or not e2:
        return False

    dx, dy = math.sub(e1.position, e2.position)

    if dx > 1:
        return False

    if dy > 1:
        return False

    if dx == 1 and dy == 1:
        return False

    return True


class math(object):
    @staticmethod
    def add(lhs, rhs):
        return lhs[0] + rhs[0], lhs[1] + rhs[1]

    @staticmethod
    def sub(lhs, rhs):
        return lhs[0] - rhs[0], lhs[1] - rhs[1]

    @staticmethod
    def distance(lhs, rhs):
        d = math.sub(lhs, rhs)
        return sqrt(d[0] ** 2 + d[1] ** 2)
