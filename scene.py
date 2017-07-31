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
from twitchchatmanager import TwitchChatManager


class TickEvent(object):
    def __init__(self):
        self.type = 'TICK'


class Scene(object):
    current_scene = None

    def __init__(self):
        self.entities = []
        self.seconds_per_tick = 2
        self.timer = 0

        self.init_scene()

    def init_scene(self):
        # Persist players in level
        self.entities = [p for p in self.entities if isinstance(p, player.Player)]
        self.entities.append(TwitchChatManager())
        #self.entities.append(dungeonmaster.DungeonMaster())
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

        # Place players near stair
        for p in [p for p in self.entities if isinstance(p, player.Player)]:
            p.max_health += 1
            p.position = self.get_location_near_stairs()

        if not Scene.current_scene:
            Scene.current_scene = self

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
        if not (x - self.level.x, y - self.level.y) in self.level.data:
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

    def update(self, time):
        for entity in self.entities:
            entity.update(time)

        self.level.update_fov()

        self.timer += time
        if self.timer > self.seconds_per_tick:
            self.timer = 0
            tdl.event.push(TickEvent())

    def get_location_near_stairs(self):
        # Find stair location
        stair_location = [e for e in self.entities if hasattr(e, 'name') and e.name == 'Stairs Up'][0].position
        stair_location = stair_location[0] - self.level.x, stair_location[1] - self.level.y

        # Find open areas around stairs
        rect = utils.rect(stair_location[0] - 3, stair_location[1] - 3, 7, 7)
        filled_location = [e.position for e in self.entities if hasattr(e, 'position')]
        possible_locations = []
        for point in rect:
            ch, fg, bg = self.level.data.get_char(*point)
            if ch == ord('.'):
                possible_locations.append(point)

        possible_locations = list(set(possible_locations).difference(set(filled_location)))
        pos = possible_locations[random.randint(0, len(possible_locations) - 1)]
        pos = pos[0] + self.level.x, pos[1] + self.level.y

        return pos
