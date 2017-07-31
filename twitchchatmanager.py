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
                        level = scene.Scene.current_scene.level

                        pos = random.randint(1, level.width - 1) + level.x, random.randint(1, level.height + level.y - 1)

                        stair_location = [e for e in scene.Scene.current_scene.entities if hasattr(e, 'name') and e.name == 'Stairs Up'][0].position
                        stair_location = stair_location[0] - scene.Scene.current_scene.level.x, stair_location[1] - scene.Scene.current_scene.level.y

                        rect = utils.rect(stair_location[0] - 2, stair_location[1] - 2, 5, 5)
                        filled_location = [e.position for e in scene.Scene.current_scene.entities if hasattr(e, 'position')]
                        possible_locations = []
                        for point in rect:
                            ch, fg, bg = scene.Scene.current_scene.level.data.get_char(*point)
                            if ch == ord('.'):
                                possible_locations.append(point)

                        possible_locations = list(set(possible_locations).difference(set(filled_location)))
                        pos = possible_locations[random.randint(0, len(possible_locations) - 1)]
                        pos = pos[0] + level.x, pos[1] + level.y

                        #while not scene.Scene.current_scene.check_collision(*pos):
                        #    pos = random.randint(1, level.width - 1) + level.x, random.randint(1, level.height + level.y - 1)

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
