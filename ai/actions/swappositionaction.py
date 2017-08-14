import utils

from ai import action


class SwapPositionAction(action.Action):
    def __init__(self, target):
        self.target = target

    def prerequisite(self, owner):
        return utils.is_next_to(owner, self.target)

    def perform(self, owner):
        self.target.position = owner.position

        # Cancel any pending actions
        if self.target.isinstance('Creature'):
            target_next_action = self.target.brain.actions[0] if self.target.brain.actions else None
            if target_next_action:
                target_next_action.fail(self.target)
