import palette
import scene

from entities import player
from ui import progressbar
from ui import window

class EntitiesWindow(window.Window):
    def __init__(self, x, y, width, height, title='Entities'):
        super().__init__(x, y, width, height, title)

    def draw(self, console):
        super().draw(console)

        row = 1
        for entity in scene.Scene.current_scene.entities:
            if isinstance(entity, player.Player):
                continue

            if hasattr(entity, 'name'):
                self.data.draw_str(1, row, '{}:{}'.format(entity.char, entity.name[:self.width - 4]), fg=entity.fg)
                row += 1

                if hasattr(entity, 'max_health') and hasattr(entity, 'current_health'):
                    pb = progressbar.ProgressBar(1, row, self.width - 2, entity.max_health, palette.BRIGHT_RED)
                    pb.draw(self.data)
                    row += 1

                row +=1

        console.blit(self.data, self.x, self.y)

    def handle_events(self, event):
        pass
