import game

from ui import console
from ui import entitieswindow
from ui import playerwindow
from ui import levelwindow

from scenes import levelscene
from scenes import scene


class GameScene(scene.Scene):
    instance = None

    def __init__(self, x=0, y=0, width=54, height=30):
        super().__init__(x, y, width, height)

        self.level_scene = None
        self.seconds_per_tick = int(game.Game.args.turn) if game.Game.args.turn else 2

        # Singleton-ish
        if not GameScene.instance:
            GameScene.instance = self

        self.init_scene()

    def init_scene(self):
        w = levelwindow.LevelWindow(11, 0, 31, 24, 'Lunch Break RL')
        w.seconds_per_tick = self.seconds_per_tick
        self.children.append(w)

        self.level_scene = levelscene.LevelScene(12, 1, 29, 22)
        self.level_scene.init_scene()
        self.children.append(self.level_scene)

        w = playerwindow.PlayerWindow(29+13, 0, 11, 30, 'Players')
        self.children.append(w)

        w = entitieswindow.EntitiesWindow(0, 0, 11, 30)
        self.children.append(w)

        con = console.Console(11, 24, 31, 6, title=None)
        self.children.append(con)
