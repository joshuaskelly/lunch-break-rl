import random

import tdl

import dungeongenerator
import game
import instances
import level
import twitchchatmanager
import utils
from scenes import scene


class LevelScene(scene.Scene):
    instance = None

    def __init__(self, x=0, y=0, width=54, height=30):
        super().__init__(x, y, width, height)

        self.level = None
        self.tick_count = 0
        self.change_level_requested = False
        self._change_level_on_tick = 0

        if not LevelScene.instance:
            LevelScene.instance = self
            instances.register('scene_root', self)

    def update(self, time):
        super().update(time)
        self.update_fov()

    def tick(self, tick):
        super().tick(tick)

        self.tick_count = tick

        if self.change_level_requested:
            instances.console.print('{} turns left.'.format(self._change_level_on_tick - tick))

            if self._change_level_on_tick - tick <= 0 or self.active_player_count() == 0:
                instances.console.print('NEXT LEVEL!')
                self.init_scene()

    def handle_events(self, event):
        super().handle_events(event)

        if game.Game.args.debug and event.type == 'KEYDOWN' and event.char.upper() == 'G':
            self.init_scene()

    def draw(self, console):
        self.console.clear()

        # Draw items
        for e in [n for n in self.children if not n.isinstance('Player') and not n.isinstance('Creature')]:
            e.draw(self.console)

        # Draw creatures
        for e in [n for n in self.children if not n.isinstance('Player') and n.isinstance('Creature')]:
            e.draw(self.console)

        # Draw players
        for e in [n for n in self.children if n.isinstance('Player')]:
            e.draw(self.console)

        console.blit(self.console, self.x, self.y, self.width, self.height)

    def init_scene(self):
        # Reset level change info
        self.change_level_requested = False
        self._change_level_on_tick = 0

        # Persist players in level
        self._children = [p for p in self.players if not p.idle]

        self.level, new_entities = dungeongenerator.generate_level(29, 22, len(self._children))
        self.append(self.level)

        # Add generated entities to scene
        for en in new_entities:
            self.append(en)

        health_bonus = len([p for p in self.players if p.state == 'EXITED'])

        # Place players near stair
        for p in self.players:
            if p.state == 'EXITED':
                # Overheal exited players up to 2x max health
                p.current_health = min(p.current_health + health_bonus, p.max_health * 2)

            p.brain.actions = []
            p.visible_tiles = set()
            p.state = 'NORMAL'
            p.brain.fail_next_action()
            p.cheer_counter = 0
            p.position = self.get_location_near_stairs()

        self.children.append(twitchchatmanager.TwitchChatManager())

    def check_collision(self, x, y):
        """Returns True if player can move into the given world coords

        x: The x-coordinate in world space
        y: The y-coordinate in world space
        """

        if (x, y) not in self.level.data:
            return False

        char, fg, bg = self.level.get_char(x, y)

        return char == ord(' ') or char == ord('.')

    def is_visibility_blocked(self, x, y):
        """Returns True if visibility is blocked at the given coord."""
        blockers = [c for c in self.children if c.blocks_visibility and c.position == (x, y)]
        if blockers:
            return True

        return not self.check_collision(x, y)

    def is_solid(self, x, y):
        return not self.check_collision(x, y)

    def get_level_entity_at(self, x, y):
        return level.LevelEntity((x, y), self.level)

    def get_entity_at(self, x, y):
        result = []
        for e in self.children:
            if hasattr(e, 'position') and e.position == (x, y):
                result.append(e)

        if not result:
            if self.is_solid(x, y):
                result.append(level.LevelEntity((x, y), self.level))

        def sort_ents(ent):
            if ent.isinstance('Creature') and not ent.isinstance('Player'):
                return 3

            elif ent.isinstance('Player'):
                return 2

            elif ent.isinstance('Corpse'):
                return 0.5

            elif ent.isinstance('Item'):
                return 1

            return 0

        result.sort(key=sort_ents, reverse=True)

        return result

    def get_entities(self, coords):
        g = self.get_entity_at
        return [entity for entity_sublist in [g(*pos) for pos in coords] for entity in entity_sublist if entity]

    def get_entities_along_path(self, x1, y1, x2, y2):
        coords = tdl.map.bresenham(x1, y1, x2, y2)
        return self.get_entities(coords)

    def check_visibility(self, x, y):
        """Returns true if given coordinate is in the player visible tiles"""
        return (x, y) in self.level.visible_tiles

    @property
    def players(self):
        return [p for p in self.children if p.isinstance('Player')]

    def active_player_count(self):
        return len([p for p in self.players if p.state != 'EXITED'])

    @property
    def downward_stair(self):
        return [e for e in self.children if e.isinstance('Stairs') and e.name == 'Down'][0]

    def change_level(self):
        if not self.change_level_requested:
            self.change_level_requested = True
            self._change_level_on_tick = self.tick_count + 30

    def get_location_near_stairs(self):
        # Find stair location
        stair_location = [e for e in self.children if e.isinstance('Stairs') and e.name == 'Up'][0].position

        # Find open areas around stairs
        rect = utils.rect(stair_location[0] - 3, stair_location[1] - 3, 7, 7)
        filled_location = [e.position for e in self.children if hasattr(e, 'position')]
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

        return pos

    def update_fov(self):
        self.level.visible_tiles = set()

        for p in self.players:
            self.level.visible_tiles = self.level.visible_tiles.union(p.visible_tiles)
            self.level.seen_tiles = self.level.seen_tiles.union(p.visible_tiles)

        if game.Game.args.debug:
            for e in [c for c in self.children if c.isinstance('Creature')]:
                self.level.visible_tiles = self.level.visible_tiles.union(e.visible_tiles)
                self.level.seen_tiles = self.level.seen_tiles.union(e.visible_tiles)

        if game.Game.args.no_fog:
            self.level.visible_tiles = self.level.visible_tiles.union([(v[0], v[1]) for v in self.level.data])
            self.level.seen_tiles = self.level.seen_tiles.union([(s[0], s[1]) for s in self.level.data])
