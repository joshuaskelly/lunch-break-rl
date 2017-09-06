import tdl

import instances
import registry

from entities.items import weapon


class Torch(weapon.Weapon):
    def __init__(self, char='t', position=(0, 0)):
        super().__init__(char, position)
        self.damage = 2
        self.name = 'torch'
        self.verb = 'burns'
        self.starting_light_radius = 7.5
        self.light_radius = 7.5
        self.timer = self.light_radius * 10

    def early_update(self, time):
        lit_tiles = tdl.map.quick_fov(self.offset[0], self.offset[1], lambda x, y: not instances.scene_root.is_visibility_blocked(x, y), radius=self.light_radius)
        instances.scene_root.level.illuminated_tiles = instances.scene_root.level.illuminated_tiles.union(lit_tiles)

    def tick(self, tick):
        self.timer -= 1
        if self.timer > 0:
            self.light_radius = self.timer / 10

        if self.timer == 0:
            if self.parent.isinstance('Creature'):
                instances.console.print('{}\'s {} goes out'.format(self.parent.display_string, self.display_string))

            else:
                instances.console.print('{} goes out'.format(self.display_string))



registry.Registry.register(Torch, 'weapon', 3)