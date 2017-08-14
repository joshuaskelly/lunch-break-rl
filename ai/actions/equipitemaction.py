import instances

from ai import action


class EquipItemAction(action.Action):
    def __init__(self, performer, target=None):
        super().__init__(performer, target)

    def prerequisite(self):
        return True

    def perform(self):
        old_item = self.performer.held_item
        old_item.position = self.target.position
        old_item.remove()
        old_item.hidden = False

        self.performer.held_item = self.target
        self.target.remove()
        self.performer.equip_held_item(self.target)

        if old_item and old_item.__class__.__name__ != 'Fist':
            if old_item.parent:
                old_item.parent.remove(old_item)

            instances.scene_root.level.append(old_item)

        if self.performer.visible:
            instances.console.print('{} is equipping {}'.format(self.performer.name, self.target.name))
