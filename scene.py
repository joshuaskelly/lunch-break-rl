import draw
import palette
import player
import level
from ui import playerwindow

from entities import item
from twitchchatmanager import TwitchChatManager

class Scene(object):
    current_scene = None

    def __init__(self):
        self.entities = []

        self.entities.append(TwitchChatManager())
        #self.entities.append(player.Player(position=(1, 1)))
        #self.entities.append(player.Player(position=(10, 10), fg=palette.BRIGHT_BLUE))
        self.level = level.Level(40, 30)

        w = playerwindow.PlayerWindow(30, 0, 10, 30, 'Players')
        self.entities.append(w)

        if not Scene.current_scene:
            Scene.current_scene = self

    def draw(self, console):
        self.level.draw(console)

        for entity in self.entities:
            entity.draw(console)

    def handle_events(self, event):
        self.level.handle_events(event)

        for entity in self.entities:
            entity.handle_events(event)

    def check_collision(self, x, y):
        char, fg, bg = self.level.get_char(x, y)

        return char != ord(' ')
