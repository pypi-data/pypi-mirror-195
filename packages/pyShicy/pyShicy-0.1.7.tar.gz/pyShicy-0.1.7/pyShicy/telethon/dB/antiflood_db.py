from .. import adB


def get_flood():
    return adB.get_key("ANTIFLOOD") or {}


def set_flood(chat_id, limit):
    omk = get_flood()
    omk.update({chat_id: limit})
    return adB.set_key("ANTIFLOOD", omk)


def get_flood_limit(chat_id):
    omk = get_flood()
    if chat_id in omk.keys():
        return omk[chat_id]


def rem_flood(chat_id):
    omk = get_flood()
    if chat_id in omk.keys():
        del omk[chat_id]
        return adB.set_key("ANTIFLOOD", omk)
