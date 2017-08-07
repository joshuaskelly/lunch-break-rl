class Registry(object):
    _registered_entities = {}

    @staticmethod
    def register(klass, type, rarity):
        type_dict = Registry._registered_entities.get(type)
        if not type_dict:
            type_dict = {}

        item_listing = type_dict.get(rarity)
        if not item_listing:
            item_listing = []

        if klass not in item_listing:
            item_listing.append(klass)

        type_dict[rarity] = item_listing
        Registry._registered_entities[type] = type_dict

    @staticmethod
    def get(type, rarity):
        type_dict = Registry._registered_entities.get(type)
        if not type_dict:
            return []

        item_listing = type_dict.get(rarity)
        if not item_listing:
            return []

        return item_listing