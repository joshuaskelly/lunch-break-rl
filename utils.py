def cp437(string):
    """Converts utf8 to codepage 437"""
    return ''.join([chr(ord(c.encode('cp437'))) for c in string])