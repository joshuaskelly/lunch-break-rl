import utils

def box(console, x, y, width, height, border=utils.cp437(' ╔╗╚╝║═')):
    for row in range(y, height + y):
        for col in range(width + x):
            if (col, row) in console:
                if col == x or col == width + x - 1:
                    console.draw_char(col, row, border[5])

                elif row == y or row == height + y - 1:
                    console.draw_char(col, row, border[6])

                else:
                    console.draw_char(col, row, border[0])

    corner_coords = (x, y), (x + width - 1, y), (x, y + height - 1), (x + width - 1, y + height - 1)
    corners = border[1:5]

    for i, c in enumerate(corner_coords):
        if c in console:
            console.draw_char(*c, corners[i])