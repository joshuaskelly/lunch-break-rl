def cp437(string):
    return ''.join([chr(ord(c.encode('cp437'))) for c in string])