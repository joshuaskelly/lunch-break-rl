colors = ((0, 0, 0), (29, 43, 83), (126, 37, 83), (0, 135, 81), (171, 82, 54), (95, 87, 79), (194, 195, 199), (255, 241, 232), (255, 0, 77), (255, 163, 0), (255, 236, 39), (0, 228, 54), (41, 173, 255), (131, 118, 156), (255, 119, 168), (255, 204, 170))

_color_cache = {}
def get_nearest(color):
    if color in _color_cache:
        return _color_cache[color]

    r, g, b = color
    result = colors[0]

    closest_dist = 999999
    for c in colors:
        r2, g2, b2 = c
        dist = (r2 - r) ** 2 + (g2 - g) ** 2 + (b2 - b) ** 2

        if dist < closest_dist:
            closest_dist = dist
            result = c

    _color_cache[color] = result
    return result

BLACK = get_nearest((0, 0, 0))
RED = get_nearest((128, 0, 0))
GREEN = get_nearest((0, 128, 0))
YELLOW = get_nearest((128, 128, 0))
BLUE = get_nearest((0, 0, 128))
MAGENTA = get_nearest((128, 0, 128))
CYAN = get_nearest((0, 128, 128))
WHITE = get_nearest((192, 192, 192))
BRIGHT_BLACK = get_nearest((128, 128, 128))
BRIGHT_RED = get_nearest((255, 0, 0))
BRIGHT_GREEN = get_nearest((0, 255, 0))
BRIGHT_YELLOW = get_nearest((255, 255, 0))
BRIGHT_BLUE = get_nearest((0, 0, 255))
BRIGHT_MAGENTA = get_nearest((255, 0, 255))
BRIGHT_CYAN = get_nearest((0, 255, 255))
BRIGHT_WHITE = get_nearest((255, 255, 255))
