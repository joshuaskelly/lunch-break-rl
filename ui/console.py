from html.parser import HTMLParser

import instances
import palette

from ui import window


class Console(window.Window):
    instance = None

    def __init__(self, x, y, width, height, title='Players'):
        super().__init__(x, y, width, height, title)

        self.messages = []
        self.colorizer = StringColorizer(palette.BRIGHT_WHITE, palette.BLACK)

        if not Console.instance:
            Console.instance = self
            instances.register('console', self)

    def print(self, message):
        self.messages.append(message)

    def describe(self, entity, visible_text, not_visible_text=None):
        if not hasattr(entity, 'visible'):
            return

        if entity.visible:
            self.print(visible_text)

        elif not_visible_text:
            self.print(not_visible_text)

    def draw(self, console):
        super().draw(console)

        row = 1
        col = 1
        for message in self.messages[-self.height+2:]:
            #self.data.draw_str(1, row, message)
            for char, fg, bg in self.colorizer.colorize(message):
                if col == self.width - 1:
                    break

                self.data.draw_char(col, row, char, fg, bg)
                col += 1

            row += 1
            col = 1

        console.blit(self.data, self.x, self.y)

    def handle_events(self, event):
        pass


class StringColorizer(HTMLParser):
    def __init__(self, fg, bg):
        super().__init__()
        self.result = []

        self._colors = [(fg, bg)]

    @property
    def current_color(self):
        return self._colors[0][0], self._colors[0][1]

    def push_color(self, color):
        self._colors.insert(0, color)

    def pop_color(self):
        self._colors.pop(0)

    def handle_starttag(self, tag, attrs):
        fg, bg = self.current_color

        if tag == 'color':
            for attr in attrs:
                key = attr[0]
                value = attr[1]
                if key == 'fg':
                    if ',' in value and value.startswith('(') and value.endswith(')'):
                        fg = tuple([int(a) for a in value[1:-1].strip(' ').split(',')])

                if key == 'bg':
                    if ',' in value and value.startswith('(') and value.endswith(')'):
                        bg = tuple([int(a) for a in value[1:-1].strip(' ').split(',')])

        self.push_color((fg, bg))

    def handle_endtag(self, tag):
        if tag == 'color':
            self.pop_color()

    def handle_data(self, data):
        processed_string = [(c, *self.current_color) for c in data]
        self.result += processed_string

    def colorize(self, message):
        self.result = []
        self.feed(message)

        return self.result
