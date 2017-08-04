import sys


class Instances(object):
    def __init__(self):
        self._instances = {}

    def register(self, name, instance):
        if name not in self._instances:
            self._instances[name] = instance

    def __getattr__(self, item):
        return self._instances[item]

sys.modules[__name__] = Instances()
