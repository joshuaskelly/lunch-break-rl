import scene

from ai import action
from entities import entity
from entities import player

class StairsDown(entity.Entity):
    def get_action(self):
        class NextLevel(action.Action):
            def prerequiste(self, owner):
                return isinstance(owner, player.Player)

            def perform(self, owner):
                scene.Scene.current_scene.init_scene()

        return NextLevel()
