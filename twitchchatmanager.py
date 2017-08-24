import time

import instances
import palette
import registry

from entities import entity
from entities.creatures import player

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
    '109thanos',
    'hawaii_beach',
    'robojester',
    'gusanolocovg',
    'newobj',
    'that_bluestone'
]


class TwitchChatManager(entity.Entity):
    def __init__(self):
        super().__init__(' ')
        self.hidden = True
        self.time_since_last_help_message = 0

    def handle_events(self, event):
        current_scene = instances.scene_root

        if event.type == 'TWITCHCHATMESSAGE':
            if event.message:
                if event.message.upper() == '!JOIN':
                    player_names = [e.name for e in current_scene.children if hasattr(e, 'name')]

                    bonus = None

                    if not event.nickname in player_names:
                        # Set player color
                        if event.tags['subscriber'] != '0' and event.nickname != 'joshuaskelly':
                            player_color = palette.BRIGHT_BLUE
                            bonus = registry.Registry.get('weapon')()

                        elif event.nickname.lower() in regular_viewers:
                            player_color = palette.BRIGHT_RED

                        else:
                            player_color = palette.get_nearest((255, 163, 0))

                        # Add player
                        pos = current_scene.get_location_near_stairs()
                        p = player.Player(event.nickname[0], pos, fg=player_color)
                        p.name = event.nickname

                        if bonus:
                            p.equip_weapon(bonus)

                        current_scene.append(p)
                        instances.console.print('{} has joined!'.format(p.display_string))

                elif event.message.upper() == '!LEAVE':
                    for e in current_scene.children:
                        if not e.isinstance('Player'):
                            continue

                        if e.name == event.nickname:
                            e.die()
                            instances.console.print('{} has left.'.format(e.display_string))

                elif event.message.upper().startswith('!CHEER'):
                    s = event.message.split(' ')
                    if len(s) <= 1:
                        return

                    player_names = [p.name for p in instances.scene_root.players if p.state != 'EXITED']
                    if event.nickname in player_names:
                        return

                    player_name = s[1].lower()
                    if player_name[0] == '@':
                        player_name = player_name[1:]

                    target_player = [p for p in instances.scene_root.players if p.state != 'EXITED' and p.name == player_name]
                    target_player = target_player[0] if target_player else None
                    if target_player:
                        target_player.cheer_counter += 4

                elif event.message.upper() == '!HELP':
                    current_time = time.time()
                    if current_time - self.time_since_last_help_message > 30:
                        help_message = 'Available commands: !join !leave !move [uldr] !move @username !stop !attack [uldr] !throw [uldr] !drop !cheer @username'
                        instances.game.observer.send_message(help_message, instances.game.channel)
                        self.time_since_last_help_message = current_time

