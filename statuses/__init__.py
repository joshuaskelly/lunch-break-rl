import registry


def register():
    registry.Registry.register(None, 'statuses', 30)
    from statuses import blindstatus
    from statuses import cowardlystatus
    from statuses import hastestatus
    from statuses import observantstatus
    from statuses import sleepstatus
