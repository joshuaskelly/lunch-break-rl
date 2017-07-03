import scene

from ai import brain
from ai import action
from entities import entity
from ui import console

class Creature(entity.Entity):
    def __init__(self, char, position=(0, 0), fg=(255, 255, 255), bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg=(0, 0, 0))
        self.brain = brain.Brain(self)
        self.name = 'Creature'
        self.current_health = 10
        self.max_health = 10

    def move(self, x, y):
        dest = self.position[0] + x, self.position[1] + y

        occupied = None

        for entity in scene.Scene.current_scene.entities:
            if not isinstance(entity, Creature):
                continue

            if dest == entity.position:
                occupied = entity
                break

        if occupied:
            console.Console.current_console.print('{} attacks {}'.format(self.name, entity.name))
            entity.current_health -= 1

        elif self.can_move(x, y):
            self.position = self.position[0] + x, self.position[1] + y

    def can_move(self, x, y):
        dest = self.position[0] + x, self.position[1] + y
        return not scene.Scene.current_scene.check_collision(*dest)

    def tick(self):
        self.brain.perform_action()

    def handle_events(self, event):
        if event.type == 'TICK':
            self.tick()
