import random

import palette
import scene
import utils

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
                        # Set player color
                        if event.tags['subscriber'] != '0' and event.nickname != 'joshuaskelly':
                            player_color = palette.BRIGHT_RED

                        elif event.nickname.lower() in regular_viewers:
                            player_color = palette.BRIGHT_BLUE

                        else:
                            player_color = palette.get_nearest((255, 163, 0))

                        # Add player
                        p = player.Player(event.nickname[0], scene.Scene.current_scene.get_location_near_stairs(), fg=player_color)
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
