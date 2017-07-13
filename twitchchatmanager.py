import random

import palette
import scene

from entities import player
from ui import console

regular_viewers = [
    'daemianend',
    'cuddigan',
    'fourbitfriday',
    'falseparklocation',
    'pythooonuser',
    'gui2203'
]

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

                        if event.nickname.lower() in regular_viewers:
                            player_color = palette.BRIGHT_BLUE

                        else:
                            player_color = palette.get_nearest((255, 163, 0))

                        p = player.Player(event.nickname[0], pos, fg=player_color)
                        p.name = event.nickname
                        s.entities.append(p)
                        console.Console.current_console.print('{} has joined!'.format(event.nickname))

                elif event.message.upper() == '!LEAVE':
                    for e in s.entities:
                        if not isinstance(e, player.Player):
                            continue

                        if e.name == event.nickname:
                            e.die()
                            console.Console.current_console.print('{} has left.'.format(event.nickname))

    def update(self, time):
        pass
