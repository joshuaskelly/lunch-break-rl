import instances
import palette

from entities import player
from ui import progressbar
from ui import window


class PlayerWindow(window.Window):
    def __init__(self, x, y, width, height, title='Players'):
        super().__init__(x, y, width, height, title)

    def draw(self, console):
        super().draw(console)

        row = 1
        for entity in instances.scene_root.children:
            if not isinstance(entity, player.Player):
                continue

            if row >= self.height - 1:
                break

            self.data.draw_str(1, row, entity.name[:self.width - 2], fg=entity.fg)

            pb = progressbar.ProgressBar(1, row + 1, self.width - 3, entity.max_health, palette.BRIGHT_RED)
            pb.current_value = entity.current_health
            pb.draw(self.data)
            
            weapon = entity.held_item
            self.data.draw_char(self.width - 2, row + 1, weapon.char, fg=weapon.fg)
            
            row += 3



        self.data.draw_str(2, self.height - 1, '(!join)', fg=palette.BRIGHT_YELLOW)
        console.blit(self.data, self.x, self.y)
