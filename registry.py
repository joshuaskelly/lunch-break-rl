import random
from bisect import bisect
from itertools import accumulate

class Registry(object):
    _registered_categories = {}

    @staticmethod
    def register(item, category, weight):
        entry = Registry._registered_categories.get(category)
        category_list = entry[0] if entry else None
        weight_table = entry[1] if entry else None

        if not category_list:
            category_list = []

        if not weight_table:
            weight_table = []

        if (item, weight) not in category_list:
            category_list.append((weight, item))

        weight_table = list(accumulate([i[0] for i in category_list]))

        Registry._registered_categories[category] = category_list, weight_table

    @staticmethod
    def get(category):
        entry = Registry._registered_categories.get(category)
        if not entry:
            return None

        category_list, weight_table = entry

        chosen = category_list[bisect(weight_table, random.random() * weight_table[-1])][1]

        return chosen

    @staticmethod
    def clear(category):
        entry = Registry._registered_categories[category] = None