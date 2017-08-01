import palette
import scene

from ai import action
from entities import entity
from entities import player

class Stairs(entity.Entity):
    def __init__(self, char='<', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)
        self.dark_fg = palette.YELLOW

    def draw(self, console):
        level = scene.Scene.current_scene.level

        if self.visible:
            console.draw_char(*self.position, self.char, self.fg, self.bg)

        elif self.position in level.seen_tiles:
            console.draw_char(*self.position, self.char, self.dark_fg, self.bg)

        for child in self.children:
            child.draw(console)

class StairsDown(Stairs):
    def __init__(self, char='>', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)
        self.dark_fg = palette.YELLOW

    def get_action(self):
        class NextLevel(action.Action):
            def prerequiste(self, owner):
                return isinstance(owner, player.Player)

            def perform(self, owner):
                scene.Scene.current_scene.init_scene()

        return NextLevel()
