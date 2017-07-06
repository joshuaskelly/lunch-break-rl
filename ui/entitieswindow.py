import palette
import scene

from entities import entity
from entities import player
from ui import progressbar
from ui import window

class EntitiesWindow(window.Window):
    def __init__(self, x, y, width, height, title='Entities'):
        super().__init__(x, y, width, height, title)

    def draw(self, console):
        super().draw(console)

        row = 1
        for e in scene.Scene.current_scene.entities:
            if isinstance(e, player.Player):
                continue

            if not (0, row) in self.data:
                break

            if isinstance(e, entity.Entity):
                self.data.draw_str(1, row, '{}:{}'.format(e.char, e.name[:self.width - 4]), fg=e.fg)
                row += 1

                if hasattr(e, 'max_health') and hasattr(e, 'current_health'):
                    pb = progressbar.ProgressBar(1, row, self.width - 2, e.max_health, palette.BRIGHT_RED)
                    pb.current_value = e.current_health
                    pb.draw(self.data)
                    row += 1

                row +=1

        console.blit(self.data, self.x, self.y)

    def handle_events(self, event):
        pass
