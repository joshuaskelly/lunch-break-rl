import instances
import palette

from ui import healthbar
from ui import window


class EntitiesWindow(window.Window):
    def __init__(self, x, y, width, height, title='Entities'):
        super().__init__(x, y, width, height, title)

    def draw(self, console):
        super().draw(console)

        row = 1
        for e in instances.scene_root.children:
            if e.isinstance('Player'):
                continue

            if row >= self.height - 1:
                break

            if e.isinstance('Entity') and e.visible and not e.isinstance('Level') and not e.isinstance('Door'):
                self.data.draw_str(1, row, '{}:{}'.format(e.char, e.name[:self.width - 4]), fg=e.fg)
                row += 1

                if hasattr(e, 'max_health') and hasattr(e, 'current_health'):
                    pb = healthbar.HealthBar(1, row, self.width - 3, e)
                    pb.current_value = e.current_health
                    pb.draw(self.data)

                    weapon = e.weapon
                    self.data.draw_char(self.width - 2, row, weapon.char, fg=weapon.fg)

                    row += 1

                row += 1

        console.blit(self.data, self.x, self.y)
