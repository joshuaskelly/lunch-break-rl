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
    dx = abs(e1.position[0] - e2.position[0])
    dy = abs(e1.position[1] - e2.position[1])

    if dx > 1:
        return False

    if dy > 1:
        return False

    if dx == 1 and dy == 1:
        return False

    return True