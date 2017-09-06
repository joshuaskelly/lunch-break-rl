class Status(object):
    def __init__(self, owner):
        self.owner = owner

    def on_status_begin(self):
        pass

    def on_status_end(self):
        pass

    def tick(self, tick):
        pass

    def remove(self):
        self.owner.remove_status(self)
