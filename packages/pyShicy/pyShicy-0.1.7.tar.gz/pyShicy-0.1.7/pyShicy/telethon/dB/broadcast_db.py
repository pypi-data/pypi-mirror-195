from .. import adB


def get_channels():  # Returns List
    return adB.get_key("BROADCAST") or []


def is_channel_added(id_):
    return id_ in get_channels()


def add_channel(id_):
    channels = get_channels()
    if id_ not in channels:
        channels.append(id_)
        adB.set_key("BROADCAST", channels)
    return True


def rem_channel(id_):
    channels = get_channels()
    if id_ in channels:
        channels.remove(id_)
        adB.set_key("BROADCAST", channels)
        return True
    return False
