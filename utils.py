def cp437(string):
    """Converts utf8 to codepage 437"""
    return ''.join([chr(ord(c.encode('cp437'))) for c in string])

def rect(x, y, width, height):
    result = []

    for i in range(width):
        for j in range(height):
            result.append((i + x, j + y))

    return result
