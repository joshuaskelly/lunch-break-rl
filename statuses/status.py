class Status(object):
    name = None

    def __init__(self, owner):
        self.owner = owner
        __class__.name = self.__class__.__name__

    def on_status_begin(self):
        pass

    def on_status_end(self):
        pass

    def tick(self, tick):
        pass

    def update(self, time):
        pass

    def stack(self, other):
        pass

    def remove(self):
        self.owner.remove_status(self)
