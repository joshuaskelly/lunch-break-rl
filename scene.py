import tdl

import dungeongenerator
import dungeonmaster
import draw
import palette
import level

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

        self.entities.append(TwitchChatManager())
        self.entities.append(dungeonmaster.DungeonMaster())
        w = levelwindow.LevelWindow(11, 0, 31, 24, 'Lunch Break RL')
        w.seconds_per_tick = self.seconds_per_tick
        self.entities.append(w)

        self.level = dungeongenerator.generate_level(29, 22) #level.Level(12, 1, 29, 22)
        self.level.x = 12
        self.level.y = 1
        self.entities.append(self.level)

        w = playerwindow.PlayerWindow(29+13, 0, 11, 30, 'Players')
        self.entities.append(w)

        w = entitieswindow.EntitiesWindow(0, 0, 11, 30)
        self.entities.append(w)

        self.console = console.Console(11, 24, 31, 6, title=None)
        self.entities.append(self.console)

        npc = kobold.Kobold(position=(15, 10))
        self.entities.append(npc)

        npc = kobold.Kobold(position=(15, 11))
        self.entities.append(npc)

        ani = animation.ThrowMotion(npc, npc.position, (25, 11), 2.0)
        npc.children.append(ani)

        i = item.Potion(char='!', position=(20, 7), fg=palette.BRIGHT_MAGENTA)
        i.name = 'potion'
        self.entities.append(i)

        i = item.Sword(position=(25, 7), fg=palette.BRIGHT_YELLOW)
        self.entities.append(i)

        i = item.Dagger(position=(15, 7), fg=palette.BRIGHT_YELLOW)
        self.entities.append(i)

        i = item.Glove(position=(17, 9))
        self.entities.append(i)

        i = item.HeldItem(char='a', position=(15, 9), fg=palette.BRIGHT_YELLOW)
        i.name = 'ax'
        i.verb  = 'chops'
        i.damage = 4
        self.entities.append(i)

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

    def check_collision(self, x, y):
        """Returns True if player can move into the given world coords

        x: The x-coordinate in world space
        y: The y-coordinate in world space
        """

        # Convert from world to local space
        if not (x - self.level.x, y - self.level.y) in self.level.data:
            return False

        char, fg, bg = self.level.get_char(x - self.level.x, y - self.level.y)

        return char == ord(' ')

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
