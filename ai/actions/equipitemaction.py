import instances

from ai import action


class EquipItemAction(action.Action):
    def __init__(self, item):
        super().__init__()
        self.item = item

    def prerequisite(self, owner):
        return True

    def perform(self, owner):
        old_item = owner.held_item
        old_item.position = self.item.position
        old_item.remove()
        old_item.hidden = False

        owner.held_item = self.item
        self.item.remove()
        owner.equip_held_item(self.item)

        if old_item and old_item.__class__.__name__ != 'Fist':
            if old_item.parent:
                old_item.parent.remove(old_item)

            instances.scene_root.level.append(old_item)

        if owner.visible:
            instances.console.print('{} is equiping {}'.format(owner.name, self.item.name))
