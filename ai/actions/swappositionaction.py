import utils

from ai import action


class SwapPositionAction(action.Action):
    def __init__(self, performer, target):
        super().__init__(performer, target)

    def prerequisite(self):
        return utils.is_next_to(self.performer, self.target)

    def perform(self):
        self.target.position = self.performer.position

        # Cancel any pending actions
        if self.target.isinstance('Creature'):
            target_next_action = self.target.brain.actions[0] if self.target.brain.actions else None
            if target_next_action:
                target_next_action.fail()
