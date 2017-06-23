class ProgressBar(object):
    def __init__(self, x, y, width, max, color):
        self.max_value = max
        self.current_value = max
        self.width = width
        self.color = color
        self.x = x
        self.y = y
        self.show_text = True

    def draw(self, console):
        bar_width = int(self.current_value / self.max_value * self.width)
        v = '{}/{}'.format(int(self.current_value), self.max_value)
        
        for i in range(self.width):
            c = ' '
            if i < len(v) and self.show_text:
                c = v[i]

            bg = 0, 0, 0
            if i <= bar_width:
                bg = self.color

            console.draw_char(self.x + i, self.y, c, bg=bg)

    def handle_events(self, event):
        pass
    
    def update(self, time):
        pass
