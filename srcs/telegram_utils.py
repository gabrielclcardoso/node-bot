import constants as const


def authorized(id):
    if str(id) != const.CHAT_ID:
        return False
    return True


async def send_message(context, msg, id=const.CHAT_ID):
    await context.bot.send_message(id, text=msg)
