import constants as const


def authorized(id):
    if str(id) != const.CHAT_ID:
        return False
    return True
