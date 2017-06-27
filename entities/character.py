import scene

from ai import brain
from ai import action
from entities import entity

class Character(entity.Entity):
    def __init__(self, char, position=(0, 0), fg=(255, 255, 255), bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg=(0, 0, 0))
        self.brain = brain.Brain(self)

    def move(self, x, y):
        dest = self.position[0] + x, self.position[1] + y

        if self.can_move(*dest):
            self.position = self.position[0] + x, self.position[1] + y

    def can_move(self, x, y):
        dest = self.position[0] + x, self.position[1] + y
        return not scene.Scene.current_scene.check_collision(*dest)

    def tick(self):
        self.brain.perform_action()

    def handle_events(self, event):
        if event.type == 'TICK':
            self.tick()
