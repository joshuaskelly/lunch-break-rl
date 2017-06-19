import utils

DEFAULT_NINE_SLICE = utils.cp437('╔═╗║ ║╚═╝')

def box(console, x, y, width, height, border=DEFAULT_NINE_SLICE):
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
                if col == x:
                    console.draw_char(col, row, border[3])
                
                elif col == width + x - 1:
                    console.draw_char(col, row, border[5])

                elif row == y:
                    console.draw_char(col, row, border[1])
                    
                elif row == height + y - 1:
                    console.draw_char(col, row, border[7])

                else:
                    console.draw_char(col, row, border[4])

    corner_coords = (x, y), (x + width - 1, y), (x, y + height - 1), (x + width - 1, y + height - 1)
    corners = [border[i] for i in [0, 2, 6, 8]]

    for i, c in enumerate(corner_coords):
        if c in console:
            console.draw_char(*c, corners[i])