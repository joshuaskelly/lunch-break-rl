import tdl

import instances

from scenes import scene


class StartLevelEvent(object):
    def __init__(self):
        self.type = 'StartLevel'


class IntermissionScene(scene.Scene):
    def __init__(self, x=0, y=0, width=54, height=30):
        super().__init__(x, y, width, height)

        self.timer = 5
        if instances.game.args.debug:
            self.timer = 1

    def update(self, time):
        pass

    def tick(self, tick):
        self.timer -= 1

        if self.timer <= 0:
            tdl.event.push(StartLevelEvent())

    def handle_events(self, event):
        pass

    def draw(self, console):
        message = 'Level {}'.format(instances.scene_root.info['level'])
        self.console.draw_str(self.console.width // 2 - len(message) // 2, self.console.height / 2, message)
        console.blit(self.console, self.x, self.y, self.width, self.height)