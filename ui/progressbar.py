class ProgressBar(object):
    def __init__(self, x, y, width, max, color):
        self.max_value = max
        self.current_value = max
        self.width = width
        self.color = color
        self.x = x
        self.y = y

    def draw(self, console):
        w = int(self.current_value / self.max_value * self.width)
        v = '{}/{}'.format(self.current_value, self.max_value)
        
        for i in range(w):
            c = ' '
            if i < len(v):
                c = v[i]
            console.draw_char(self.x + i, self.y, c, bg=self.color)

    def handle_events(self, event):
        pass
    
    def update(self, time):
        pass
