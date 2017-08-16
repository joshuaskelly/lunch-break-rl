import palette

from entities import item


class Consumable(item.UsableItem):
    def __init__(self, char='!', position=(0, 0), fg=palette.BRIGHT_MAGENTA, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)
