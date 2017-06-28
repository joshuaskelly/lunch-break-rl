import random

import palette
import scene

from entities import player

class TwitchChatManager(object):
    def draw(self, console):
        pass

    def handle_events(self, event):
        s = scene.Scene.current_scene

        if event.type == 'TWITCHCHATMESSAGE':
            if event.message:
                if event.message.upper() == '!JOIN':
                    p = player.Player(event.nickname[0], (1, 20), palette.colors[random.randint(1, len(palette.colors) - 1)])
                    p.nickname = event.nickname
                    s.entities.append(p)

                elif event.message.upper() == '!LEAVE':
                    for entity in s.entities:
                        if not isinstance(entity, player.Player):
                            continue

                        if entity.nickname == event.nickname:
                            s.entities.remove(entity)

    def update(self, time):
        pass
