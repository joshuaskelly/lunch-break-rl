import scene

from ai import brain
from ai import action
from entities import entity
from entities import item
from ui import console

class Creature(entity.Entity):
    def __init__(self, char, position=(0, 0), fg=(255, 255, 255), bg=(0, 0, 0)):
        super().__init__(char, position, fg, bg=(0, 0, 0))
        self.brain = brain.Brain(self)
        self.name = 'Creature'
        self.current_health = 10
        self.max_health = 10
        self.held_item = item.Fist('f')

    def move(self, x, y):
        dest = self.position[0] + x, self.position[1] + y

        action_to_perform = None

        for e in scene.Scene.current_scene.entities:
            if not isinstance(e, entity.Entity):
                continue

            if dest == e.position:
                action_to_perform = e.get_action()

        if action_to_perform and action_to_perform.prerequiste(self):
            action_to_perform.perform(self)

        elif self.can_move(x, y):
            self.position = self.position[0] + x, self.position[1] + y

    def can_move(self, x, y):
        dest = self.position[0] + x, self.position[1] + y
        return not scene.Scene.current_scene.check_collision(*dest)

    def update(self, time):
        if self.current_health <= 0:
            self.die()

    def die(self):
        if self.held_item != item.Fist:
            i = self.held_item
            i.position = self.position
            scene.Scene.current_scene.entities.append(i)
            
        console.Console.current_console.print('{} perishes!'.format(self.name))
        self.remove()

    def tick(self):
        self.brain.perform_action()

    def handle_events(self, event):
        if event.type == 'TICK':
            self.tick()

    def get_action(self):
        return action.AttackAction(self)