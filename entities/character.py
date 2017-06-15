import scene

from entities import entity

class Character(entity.Entity):
    def move(self, x, y):
        dest = self.position[0] + x, self.position[1] + y

        if not scene.Scene.current_scene.check_collision(dest[0], dest[1]):
            self.position = self.position[0] + x, self.position[1] + y
