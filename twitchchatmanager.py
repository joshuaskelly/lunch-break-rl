import random

import palette
import scene

from entities import player
from ui import console

class TwitchChatManager(object):
    def draw(self, console):
        pass

    def handle_events(self, event):
        s = scene.Scene.current_scene

        if event.type == 'TWITCHCHATMESSAGE':
            if event.message:
                if event.message.upper() == '!JOIN':
                    player_names = [e.name for e in s.entities if hasattr(e, 'name')]

                    if not event.nickname in player_names:
                        level = scene.Scene.current_scene.level
                        pos = level.x + random.randint(0, 10), level.y + random.randint(0, 10)
                        p = player.Player(event.nickname[0], pos, palette.colors[random.randint(1, len(palette.colors) - 1)])
                        p.name = event.nickname
                        s.entities.append(p)
                        console.Console.current_console.print('{} has joined!'.format(event.nickname))

                elif event.message.upper() == '!LEAVE':
                    for entity in s.entities:
                        if not isinstance(entity, player.Player):
                            continue

                        if entity.name == event.nickname:
                            s.entities.remove(entity)
                            console.Console.current_console.print('{} has left.'.format(event.nickname))

    def update(self, time):
        pass
