import instances
import palette

from ai import action
from entities import entity


class Stairs(entity.Entity):
    def __init__(self, char='<', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)
        self.fog_color = palette.YELLOW
        self.name = 'Up'

    def allow_throw(self, action):
        return False


class StairsDown(Stairs):
    def __init__(self, char='>', position=(0, 0), fg=palette.BRIGHT_YELLOW, bg=palette.BLACK):
        super().__init__(char, position, fg, bg)
        self.dark_fg = palette.YELLOW
        self.name = 'Down'
        self._countdown_timer = 10
        self._countdown_started = False

    def tick(self, tick):
        if self.visible and not self._countdown_started:
            self._countdown_started = True
            instances.console.print('Gloom spreads through the halls')

        if self._countdown_started:
            self._countdown_timer -= 1

        if self._countdown_timer <= 0:
            instances.scene_root.start_darkness()

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
