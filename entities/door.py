import instances
import palette

from entities import entity


class Door(entity.Entity):
    def __init__(self, char='+', position=(0, 0)):
        super().__init__(char, position, fg=palette.get_nearest((171, 82, 54)))
        self.blocks_visibility = True
        self.fog_color = palette.get_nearest((95, 87, 79))
