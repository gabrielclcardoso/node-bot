from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler
import logging

import constants as const
import mixnet_query as mx_query


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

MIXNODES = []
GATEWAYS = []


def main():
    application = Application.builder().token(const.TOKEN).build()

    add_mixnode_handler = CommandHandler('addmix', add_mixnode)
    add_gateway_handler = CommandHandler('addgate', add_gateway)
    mixnode_handler = CommandHandler('mixscore', mixnode_score)
    gateway_handler = CommandHandler('gatescore', gateway_score)

    application.add_handler(add_mixnode_handler)
    application.add_handler(add_gateway_handler)
    application.add_handler(mixnode_handler)
    application.add_handler(gateway_handler)

    job_queue = application.job_queue
    job_queue.run_repeating(print_nodes, interval=5)

    application.run_polling()


async def gateway_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for gateway in context.args:
        try:
            score = mx_query.get_node_score(gateway, "gateway")
            await context.bot.send_message(chat_id=const.CHAT_ID, text=score)
        except Exception as e:
            msg = f'Error fetching score of gateway {gateway}:\n\n{e}'
            await context.bot.send_message(chat_id=const.CHAT_ID, text=msg)


async def mixnode_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for mixnode in context.args:
        try:
            score = mx_query.get_node_score(mixnode, "mixnode")
            await context.bot.send_message(chat_id=const.CHAT_ID, text=score)
        except Exception as e:
            msg = f'Error fetching score of mixnode {mixnode}:\n\n{e}'
            await context.bot.send_message(chat_id=const.CHAT_ID, text=msg)


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


async def print_nodes(context: ContextTypes.DEFAULT_TYPE):
    for mixnode in MIXNODES:
        await context.bot.send_message(chat_id=const.CHAT_ID, text=mixnode)

    for gateway in GATEWAYS:
        await context.bot.send_message(chat_id=const.CHAT_ID, text=gateway)

if __name__ == '__main__':
    main()
