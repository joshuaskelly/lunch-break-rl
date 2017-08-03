import random

import tdl

import dungeongenerator
import dungeonmaster
import draw
import palette
import level
import utils

from ui import console
from ui import entitieswindow
from ui import playerwindow
from ui import levelwindow

from ai import action
from entities import animation
from entities import entity
from entities import item
from entities import kobold
from entities import player
from entities import stairs
from twitchchatmanager import TwitchChatManager


class TickEvent(object):
    def __init__(self, tick_number):
        self.type = 'TICK'
        self.tick_number = tick_number


class Scene(object):
    current_scene = None

    def __init__(self):
        self.entities = []
        self.seconds_per_tick = 2
        self.timer = 0
        self.tick_count = 0
        self.change_level_requested = False
        self._change_level_on_tick = 0

        self.init_scene()

    def init_scene(self):
        # Persist players in level
        self.change_level_requested = False
        self._change_level_on_tick = 0

        self.entities = [p for p in self.players if not p.idle]
        self.entities.append(TwitchChatManager())
        w = levelwindow.LevelWindow(11, 0, 31, 24, 'Lunch Break RL')
        w.seconds_per_tick = self.seconds_per_tick
        self.entities.append(w)

        self.level, new_entities = dungeongenerator.generate_level(29, 22) #level.Level(12, 1, 29, 22)
        self.level.x = 12
        self.level.y = 1
        self.entities.append(self.level)

        w = playerwindow.PlayerWindow(29+13, 0, 11, 30, 'Players')
        self.entities.append(w)

        w = entitieswindow.EntitiesWindow(0, 0, 11, 30)
        self.entities.append(w)

        self.console = console.Console(11, 24, 31, 6, title=None)
        self.entities.append(self.console)

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

        if not Scene.current_scene:
            Scene.current_scene = self

    def change_level(self):
        if not self.change_level_requested:
            self.change_level_requested = True
            self._change_level_on_tick = self.tick_count + 30

    def draw(self, console):
        for e in [n for n in self.entities if not isinstance(n, player.Player)]:
            e.draw(console)

        for e in [n for n in self.entities if isinstance(n, player.Player)]:
            e.draw(console)

    def handle_events(self, event):
        for e in self.entities:
            e.handle_events(event)

            if event.type == 'KEYDOWN':
                if event.keychar.upper() == 'G':
                    self.init_scene()

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

    def tick(self, tick_number):
        if self.change_level_requested:
            console.Console.current_console.print('{} turns left.'.format(self._change_level_on_tick - tick_number))


            if self._change_level_on_tick - tick_number <= 0 or self.active_player_count() == 0:
                console.Console.current_console.print('NEXT LEVEL!')
                self.init_scene()

    def update(self, time):
        for entity in self.entities:
            entity.update(time)

        self.level.update_fov()

        self.timer += time
        if self.timer > self.seconds_per_tick:
            self.timer = 0
            self.tick_count += 1
            self.tick(self.tick_count)
            tdl.event.push(TickEvent(self.tick_count))

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
