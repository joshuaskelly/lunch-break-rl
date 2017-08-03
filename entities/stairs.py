import palette
import scene

from ai import action
from entities import entity
from entities import player

class Stairs(entity.Entity):
    def __init__(self, char='<', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)
        self.dark_fg = palette.YELLOW
        self.name = 'Up'

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
        self.name = 'Down'

    def get_action(self, other=None):
        if not isinstance(other, player.Player):
            return None

        class NextLevel(action.Action):
            def prerequiste(self, owner):
                return isinstance(owner, player.Player)

            def perform(self, owner):
                owner.current_health = owner.max_health
                owner.state = 'EXITED'
                owner.position = -1, -1

                # TODO: Fix the below
                # Start a countdown timer
                scene.Scene.current_scene.change_level()

        return NextLevel()
