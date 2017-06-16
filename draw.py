import utils

def box(console, x, y, width, height, border=utils.cp437(' ╔╗╚╝║═')):
    """Draws a box on the given console.

    Args:
        x: The leftmost column of the box.

        y: The topmost column of the box.

        width: The width of the box.

        height: The height of the box.

        border: A string that contains the characters to render the box. The
            order should be:
                0. inside
                1. top left corner
                2. top right corner
                3. bottom left corner
                4. bottom right corner
                5. vertical bar
                6. horizontal bar
    """

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