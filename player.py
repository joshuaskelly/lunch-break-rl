class Player(object):
    def __init__(self):
        self.position = 0, 0

    def draw(self, console):
        if self.position in console:
            console.set_colors(fg=(255,0,0))
            console.draw_char(self.position[0], self.position[1], '@')
            console.set_colors(fg=(255,255,255))

    def update(self):
        pass

    def handle_events(self, event):
        if event.type == 'KEYDOWN':
            if event.keychar.upper() == 'UP':
                self.position = self.position[0], self.position[1] - 1

            elif event.keychar.upper() == 'DOWN':
                self.position = self.position[0], self.position[1] + 1

            elif event.keychar.upper() == 'LEFT':
                self.position = self.position[0] - 1, self.position[1]

            elif event.keychar.upper() == 'RIGHT':
                self.position = self.position[0] + 1, self.position[1]
