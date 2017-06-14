import tdl

class Level(object):
    def __init__(self, width, height):
        self.data = tdl.Console(width, height)
        self.painting = False
        self.erasing = False

    def draw_char(self, x, y, fg=Ellipsis, bg=Ellipsis):
        self.data.draw_char(x, y, fg, bg)

    def get_char(self, x, y):
        return self.data.get_char(x, y)

    def draw(self, console):
        console.blit(self.data)

    def handle_events(self, event):
        if event.type == 'MOUSEDOWN':
            if event.button == 'LEFT':
                if not self.erasing:
                    self.painting = True

            if event.button == 'RIGHT':
                if not self.painting:
                    self.erasing = True

        if event.type == 'MOUSEUP':
            if event.button == 'LEFT':
                if not self.erasing:
                    self.painting = False

            if event.button == 'RIGHT':
                if not self.painting:
                    self.erasing = False

        if event.type == 'MOUSEMOTION':
            pos = event.cell

            if self.painting:
                self.draw_char(*pos, '#')

            elif self.erasing:
                self.draw_char(*pos, ' ')
