import random

import dungeongenerator
import instances
import utils

from entities import player
from entities import stairs
from scenes import scene


class LevelScene(scene.Scene):
    instance = None

    def __init__(self):
        super().__init__()

        self.level = None
        self.tick_count = 0
        self.change_level_requested = False
        self._change_level_on_tick = 0

        if not LevelScene.instance:
            LevelScene.instance = self
            instances.register('scene_root', self)

    def update(self, time):
        super().update(time)
        self.level.update_fov()

    def tick(self, tick):
        super().tick(tick)

        self.tick_count = tick

        if self.change_level_requested:
            instances.console.print('{} turns left.'.format(self._change_level_on_tick - tick))

            if self._change_level_on_tick - tick <= 0 or self.active_player_count() == 0:
                instances.console.print('NEXT LEVEL!')
                self.init_scene()

    def draw(self, console):
        # Draw items and creatures
        for e in [n for n in self.entities if not isinstance(n, player.Player)]:
            e.draw(console)

        # Draw players
        for e in [n for n in self.entities if isinstance(n, player.Player)]:
            e.draw(console)

    def init_scene(self):
        # Reset level change info
        self.change_level_requested = False
        self._change_level_on_tick = 0

        # Persist players in level
        self.entities = [p for p in self.players if not p.idle]

        self.level, new_entities = dungeongenerator.generate_level(29, 22)
        self.level.x = 12
        self.level.y = 1
        self.entities.append(self.level)

        # Add generated entities to scene
        for en in new_entities:
            pos = en.position
            pos = pos[0] + self.level.x, pos[1] + self.level.y
            en.position = pos

            self.entities.append(en)

        health_bonus = len([p for p in self.players if p.state == 'EXITED'])

        # Place players near stair
        for p in self.players:
            if p.state == 'EXITED':
                p.max_health += health_bonus
                p.current_health += health_bonus

            p.brain.actions = []
            p.visible_tiles = set()
            p.state = 'NORMAL'

            pos = self.get_location_near_stairs()

            p.position = pos

    def check_collision(self, x, y):
        """Returns True if player can move into the given world coords

        x: The x-coordinate in world space
        y: The y-coordinate in world space
        """

        # Convert from world to local space
        if (x - self.level.x, y - self.level.y) not in self.level.data:
            return False

        char, fg, bg = self.level.get_char(x - self.level.x, y - self.level.y)

        return char == ord(' ') or char == ord('.')

    def is_solid(self, x, y):
        return not self.check_collision(x, y)

    def get_entity_at(self, x, y):
        result = []
        for e in self.entities:
            if hasattr(e, 'position') and e.position == (x, y):
                result.append(e)

        return result

    def check_visibility(self, x, y):
        return (x, y) in self.level.visible_tiles

    @property
    def players(self):
        return [p for p in self.entities if isinstance(p, player.Player)]

    def active_player_count(self):
        return len([p for p in self.players if p.state != 'EXITED'])

    def change_level(self):
        if not self.change_level_requested:
            self.change_level_requested = True
            self._change_level_on_tick = self.tick_count + 30

    def get_location_near_stairs(self):
        # Find stair location
        stair_location = [e for e in self.entities if isinstance(e, stairs.Stairs) and e.name == 'Up'][0].position
        stair_location = stair_location[0] - self.level.x, stair_location[1] - self.level.y

        # Find open areas around stairs
        rect = utils.rect(stair_location[0] - 3, stair_location[1] - 3, 7, 7)
        filled_location = [e.position for e in self.entities if hasattr(e, 'position')]
        possible_locations = []
        for point in rect:
            if point not in self.level.data:
                continue

            ch, fg, bg = self.level.data.get_char(*point)
            if ch == ord('.'):
                possible_locations.append(point)

        possible_locations = list(set(possible_locations).difference(set(filled_location)))

        if not possible_locations:
            raise RuntimeError('Unable to find empty space around stairs up')

        pos = possible_locations[random.randint(0, len(possible_locations) - 1)]
        pos = pos[0] + self.level.x, pos[1] + self.level.y

        return pos
