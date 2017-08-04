import configparser
import os
import time

import tdl
from twitchobserver import Observer

from scenes.gamescene import GameScene


class TickEvent(object):
    def __init__(self, tick_number):
        self.type = 'TICK'
        self.tick_number = tick_number


class Game(object):
    args = None
    scene_root = None
    config = None

    def __init__(self, args):
        Game.args = args

        # Configure game settings
        config = configparser.ConfigParser()
        cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.cfg')
        config.read(cfg_path)
        Game.config = config

        # Configure tdl
        tdl.set_font('terminal32x32_gs_ro.png')
        tdl.set_fps(int(Game.config['ENGINE']['fps']))
        self.console = tdl.init(54, 30, 'lunch break roguelike', renderer=Game.config['ENGINE']['renderer'])
        self._last_time = time.time()

        # Set static attributes
        Game.scene_root = GameScene()

        # Twitch Observer
        nickname = Game.config['TWITCH']['Nickname']
        password = Game.config['TWITCH']['Password']
        channel = Game.config['TWITCH']['Channel']
        self.observer = Observer(nickname, password)
        self.observer.start()
        self.observer.join_channel(channel)

    def run(self):
        tick_count = 0
        timer = 0
        last_time = 0
        seconds_per_tick = int(Game.config['GAME']['turn'])

        running = True
        while running:
            # Draw the scene
            self.console.clear()
            Game.scene_root.draw(self.console)
            tdl.flush()

            # Handle input/events
            for event in list(tdl.event.get()) + self.observer.get_events():
                Game.scene_root.handle_events(event)

                if event.type == 'QUIT':
                    running = False
                    self.observer.stop()

            # Update scene
            time_elapsed = time.time() - last_time
            timer += time_elapsed
            last_time = time.time()
            Game.scene_root.update(time_elapsed)

            # Send out tick event
            if timer > seconds_per_tick:
                timer = 0
                tick_count += 1
                Game.scene_root.tick(tick_count)

