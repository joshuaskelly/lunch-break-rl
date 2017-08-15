import palette

from entities import entity


class HealthBar(entity.Entity):
    def __init__(self, x, y, width, target):
        super().__init__(' ', position=(x, y))

        self.target = target
        self.max_value = self.target.max_health
        self.current_value = self.target.current_health
        self.width = width
        self.x = x
        self.y = y
        self.show_text = True
        self.color = palette.BRIGHT_GREEN

    def draw(self, console):
        bar_width = int(self.current_value / self.max_value * self.width) - 1
        display_text = ' {}/{}'.format(int(self.current_value), self.max_value)

        percentage = self.current_value / self.max_value

        if percentage > 1.0:
            self.color = palette.BRIGHT_BLUE
        elif percentage > 0.75:
            self.color = palette.BRIGHT_GREEN
        elif percentage > 0.5:
            self.color = palette.BRIGHT_YELLOW
        elif percentage > 0.25:
            self.color = palette.get_nearest((255, 163, 0))
        else:
            self.color = palette.BRIGHT_RED

        for i in range(self.width):
            c = ' '
            if i < len(display_text) and self.show_text:
                c = display_text[i]

            bg = 0, 0, 0
            if i <= bar_width:
                bg = self.color

            console.draw_char(self.x + i, self.y, c, bg=bg)

    def handle_events(self, event):
        pass

    def update(self, time):
        pass
