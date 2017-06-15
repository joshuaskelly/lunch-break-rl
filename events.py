class Event(object):
    events = {}

    @classmethod
    def subscribe(cls, msg, callback):
        if msg in cls.events:
            cls.events[msg].append(callback)

        else:
            cls.events[msg] = [callback]

    @classmethod
    def unsubscribe(cls, msg, callback):
        if msg in cls.events:
            try:
                cls.events[msg].pop(cls.events[msg].index(callback))

            except ValueError:
                pass

    @classmethod
    def notify(cls, msg, *args, **kwargs):
        for func in cls.events[msg]:
            func(*args, **kwargs)
