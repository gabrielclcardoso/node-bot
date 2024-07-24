from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler
import logging
from textwrap import dedent

import constants as const
import mixnet_query as mx_query
import data


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

try:
    MIXNODES = data.load_mixnodes()
except Exception:
    MIXNODES = []
try:
    GATEWAYS = data.load_gateways()
except Exception:
    GATEWAYS = []


def main():
    application = Application.builder().token(const.TOKEN).build()

    add_mixnode_handler = CommandHandler('addmix', add_mixnode)
    del_mixnode_handler = CommandHandler('delmix', del_mixnode)
    add_gateway_handler = CommandHandler('addgate', add_gateway)
    del_gateway_handler = CommandHandler('delgate', del_gateway)

    application.add_handler(add_mixnode_handler)
    application.add_handler(del_mixnode_handler)
    application.add_handler(add_gateway_handler)
    application.add_handler(del_gateway_handler)

    job_queue = application.job_queue
    job_queue.run_repeating(report_nodes, interval=5)

    application.run_polling()


async def add_mixnode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != const.CHAT_ID:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Unauthorized")

    for mixnode in context.args:
        if mx_query.node_exists(mixnode, 'mixnode'):
            MIXNODES.append(mixnode)
            msg = f'Added mixnode {mixnode} to watchlist'
        else:
            msg = f'Mixnode {mixnode} does not exist or API is not reachable'
        await context.bot.send_message(chat_id=const.CHAT_ID, text=msg)

    try:
        data.update_mixnodes(MIXNODES)
    except Exception as e:
        msg = f'Failed to update mixnodes file:\n\n{e}'
        await context.bot.send_message(chat_id=const.CHAT_ID, text=msg)


async def del_mixnode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != const.CHAT_ID:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Unauthorized")

    for mixnode in context.args:
        try:
            MIXNODES.remove(mixnode)
            msg = f'Removed mixnode {mixnode}'
            await context.bot.send_message(chat_id=const.CHAT_ID, text=msg)
        except Exception:
            pass

    try:
        data.update_mixnodes(MIXNODES)
    except Exception as e:
        msg = f'Failed to update mixnodes file:\n\n{e}'
        await context.bot.send_message(chat_id=const.CHAT_ID, text=msg)


async def add_gateway(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != const.CHAT_ID:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Unauthorized")

    for gateway in context.args:
        if mx_query.node_exists(gateway, 'gateway'):
            GATEWAYS.append(gateway)
            msg = f'Added gateway {gateway} to watchlist'
        else:
            msg = f'Gateway {gateway} does not exist or API is not reachable'
        await context.bot.send_message(chat_id=const.CHAT_ID, text=msg)

    try:
        data.update_gateways(GATEWAYS)
    except Exception as e:
        msg = f'Failed to update gateways file:\n\n{e}'
        await context.bot.send_message(chat_id=const.CHAT_ID, text=msg)


async def del_gateway(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != const.CHAT_ID:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Unauthorized")

    for gateway in context.args:
        try:
            GATEWAYS.remove(gateway)
            msg = f'Removed gateway {gateway}'
            await context.bot.send_message(chat_id=const.CHAT_ID, text=msg)
        except Exception:
            pass

    try:
        data.update_gateways(GATEWAYS)
    except Exception as e:
        msg = f'Failed to update gateways file:\n\n{e}'
        await context.bot.send_message(chat_id=const.CHAT_ID, text=msg)


async def report_nodes(context: ContextTypes.DEFAULT_TYPE):
    for mixnode in MIXNODES:
        score = mx_query.get_node_score(mixnode, 'mixnode')
        if score < const.MIN_SCORE:
            msg = f"""
                Mixnode {mixnode} having issues, current routing score: {score}
                \nExplorer: {const.MIXNODE_EXPLORER}{mixnode}
                """
            await context.bot.send_message(chat_id=const.CHAT_ID,
                                           text=dedent(msg))

    for gateway in GATEWAYS:
        score = mx_query.get_node_score(gateway, 'gateway')
        if score < const.MIN_SCORE:
            msg = f"""
                Gateway {gateway} having issues, current routing score: {score}
                \nExplorer: {const.GATEWAY_EXPLORER}{gateway}
                """
            await context.bot.send_message(chat_id=const.CHAT_ID,
                                           text=dedent(msg))

if __name__ == '__main__':
    main()
