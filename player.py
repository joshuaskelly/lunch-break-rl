import scene

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

    def move(self, x, y):
        dest = self.position[0] + x, self.position[1] + y

        if not scene.Scene.current_scene.check_collision(dest[0], dest[1]):
            self.position = self.position[0] + x, self.position[1] + y

    def handle_events(self, event):
        if event.type == 'KEYDOWN':
            if event.keychar.upper() == 'UP':
                self.move(0, -1)

            elif event.keychar.upper() == 'DOWN':
                self.move(0, 1)

            elif event.keychar.upper() == 'LEFT':
                self.move(-1, 0)

            elif event.keychar.upper() == 'RIGHT':
                self.move(1, 0)
