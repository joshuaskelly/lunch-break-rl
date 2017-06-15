from entities import character

class Player(character.Character):
    def __init__(self):
        super().__init__('@', fg=(255, 0, 0))

    def update(self):
        pass

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
