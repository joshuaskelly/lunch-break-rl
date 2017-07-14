import configparser
import os
import time

import tdl

from twitchobserver import Observer

from scene import Scene

tdl.set_font('terminal32x32_gs_ro.png')
console = tdl.init(54, 30, 'lunch break roguelike', renderer='OPENGL')
tdl.set_fps(30)

scene = Scene()

last_time = time.time()

# Twitch Observer
config = configparser.ConfigParser()
cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'chat.cfg')
config.read(cfg_path)
nickname = config['DEFAULT']['Nickname']
password = config['DEFAULT']['Password']
channel = config['DEFAULT']['Channel']
observer = Observer(nickname, password)
observer.start()
observer.join_channel(channel)

running = True
while running:
    # Draw the scene
    console.clear()
    scene.draw(console)
    tdl.flush()

    # Handle input/events
    for event in list(tdl.event.get()) + observer.get_events():
        scene.handle_events(event)

        if event.type == 'QUIT':
            running = False
            observer.stop()

    scene.update(time.time() - last_time)
    last_time = time.time()
