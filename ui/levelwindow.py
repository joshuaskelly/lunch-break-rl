import palette

from ui import progressbar
from ui import window

class LevelWindow(window.Window):
    def __init__(self, x, y, width, height, title):
        super().__init__(x, y, width, height, title)

        progressbar_width = 10
        self.progressbar = progressbar.ProgressBar(width // 2 - progressbar_width // 2, height-1, progressbar_width, 100, palette.BRIGHT_BLUE)
        self.progressbar.show_text = False
        self.children.append(self.progressbar)
        self.time = 0

    def draw(self, console):
        super().draw(console)
    
    def update(self, time):
        super().update(time)

        self.time += time
        v = self.time * 95.23 % self.progressbar.max_value
        self.progressbar.current_value = v
