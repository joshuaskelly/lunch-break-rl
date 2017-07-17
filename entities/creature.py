import tdl

import palette
import scene

from ai import brain
from ai import action
from entities import animation
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
        self.visible_tiles = set()

    def move(self, x, y):
        dest = self.position[0] + x, self.position[1] + y

        action_to_perform = None
        target_entity = None

        for e in scene.Scene.current_scene.entities:
            if not isinstance(e, entity.Entity):
                continue

            if dest == e.position:
                action_to_perform = e.get_action()
                target_entity = e
                break

        if action_to_perform and action_to_perform.prerequiste(self):
            action_to_perform.perform(self)

            next_action = self.brain.actions[0]
            if isinstance(next_action, action.MoveAction) and next_action.parent:
                next_action.fail(self)

        if target_entity and target_entity.position == dest:
            return

        if self.can_move(x, y):
            self.position = self.position[0] + x, self.position[1] + y

    def can_move(self, x, y):
        dest = self.position[0] + x, self.position[1] + y
        return scene.Scene.current_scene.check_collision(*dest)

    def update(self, time):
        if self.current_health <= 0:
            self.die()

        super().update(time)

    def update_fov(self):
        x, y = self.position
        self.visible_tiles = tdl.map.quick_fov(x, y, scene.Scene.current_scene.check_collision)

    def drop_held_item(self):
        if not isinstance(self.held_item, item.Fist):
            i = self.held_item
            i.position = self.position
            scene.Scene.current_scene.entities.append(i)
            self.held_item = item.Fist('f')

    def hurt(self, damage, hurt_action):
        self.current_health -= damage
        ani = animation.FlashBackground(bg=palette.BRIGHT_RED)
        ani.parent = self
        self.children.append(ani)

        if self.current_health > 0 and hasattr(self.held_item, 'on_hurt'):
            self.held_item.on_hurt(damage, hurt_action)

    def die(self):
        self.drop_held_item()
        console.Console.current_console.print('{} perishes!'.format(self.name))
        self.remove()

    def tick(self):
        self.brain.perform_action()
        self.update_fov()

    def handle_events(self, event):
        if event.type == 'TICK':
            self.tick()

        super().handle_events(event)

    def get_action(self):
        return action.AttackAction(self)

    @property
    def visible_entities(self):
        current_scene = scene.Scene.current_scene
        result = []

        for e in current_scene.entities:
            if not isinstance(e, entity.Entity):
                continue

            if e == self:
                continue

            if e.position in self.visible_tiles:
                result.append(e)

        return result
