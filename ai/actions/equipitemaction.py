import instances

from ai import action


class EquipItemAction(action.Action):
    def __init__(self, performer, target=None):
        super().__init__(performer, target)

    def prerequisite(self):
        return self.performer.can_equip(self.target)

    def perform(self):
        old_item = self.performer.weapon
        old_item.position = self.target.position
        old_item.remove()
        old_item.hidden = False

        self.performer.weapon = self.target
        self.target.remove()
        self.performer.equip_weapon(self.target)

        if old_item and old_item.__class__.__name__ != 'Fist':
            if old_item.parent:
                old_item.parent.remove(old_item)

            instances.scene_root.level.append(old_item)

        if self.performer.visible:
            instances.console.describe(self.performer, '{} picks up {}'.format(self.performer.display_string, self.target.display_string))


class EquipItemInterface(object):
    def can_equip(self, target):
        """Determines if performer can equip target"""
        return True
