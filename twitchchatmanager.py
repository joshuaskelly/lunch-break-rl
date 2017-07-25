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
    'gui2203',
    'nimphious',
    'loggercito'
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

                        pos = random.randint(1, level.width - 1) + level.x, random.randint(1, level.height + level.y - 1)
                        while not scene.Scene.current_scene.check_collision(*pos):
                            pos = random.randint(1, level.width - 1) + level.x, random.randint(1, level.height + level.y - 1)

                        if event.tags['subscriber'] != '0' and event.nickname != 'joshuaskelly':
                            player_color = palette.get_nearest((131, 118, 156))

                        elif event.nickname.lower() in regular_viewers:
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
