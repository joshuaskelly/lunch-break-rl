import palette
from entities import player, entity
from scenes import gamescene
from ui import console

regular_viewers = [
    'daemianend',
    'cuddigan',
    'fourbitfriday',
    'falseparklocation',
    'pythooonuser',
    'gui2203',
    'nimphious',
    'loggercito',
    'firedrgn',
    'kingdred405',
    'slayerdarth',
    'smyyth',
    'paspartout',
    'nixrod',
    'glasscaskettv',
    '109thanos'
]

class TwitchChatManager(entity.Entity):
    def __init__(self):
        super().__init__(' ')

    def handle_events(self, event):
        s = gamescene.GameScene.current_scene.level_scene

        if event.type == 'TWITCHCHATMESSAGE':
            if event.message:
                if event.message.upper() == '!JOIN':
                    player_names = [e.name for e in s.entities if hasattr(e, 'name')]

                    if not event.nickname in player_names:
                        # Set player color
                        if event.tags['subscriber'] != '0' and event.nickname != 'joshuaskelly':
                            player_color = palette.BRIGHT_BLUE

                        elif event.nickname.lower() in regular_viewers:
                            player_color = palette.BRIGHT_RED

                        else:
                            player_color = palette.get_nearest((255, 163, 0))

                        # Add player
                        p = player.Player(event.nickname[0], gamescene.GameScene.current_scene.level_scene.get_location_near_stairs(), fg=player_color)
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
