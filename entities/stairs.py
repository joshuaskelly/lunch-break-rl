import instances
import palette

from ai import action
from entities import entity


class Stairs(entity.Entity):
    def __init__(self, char='<', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)
        self.dark_fg = palette.YELLOW
        self.name = 'Up'

    def draw(self, console):
        level = instances.scene_root.level

        if self.visible:
            console.draw_char(*self.offset, self.char, self.fg, self.bg)

        elif self.position in level.seen_tiles:
            console.draw_char(*self.offset, self.char, self.dark_fg, self.bg)

        for child in self.children:
            child.draw(console)


class StairsDown(Stairs):
    def __init__(self, char='>', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg)
        self.dark_fg = palette.YELLOW
        self.name = 'Down'

    def get_action(self, requester=None):
        if not requester.isinstance('Player'):
            return None

        class NextLevel(action.Action):
            def prerequisite(self):
                return self.performer.isinstance('Player')

            def perform(self):
                self.performer.state = 'EXITED'
                self.performer.position = -2, -2

                # Start a countdown timer
                instances.scene_root.change_level()

        return NextLevel(requester)
