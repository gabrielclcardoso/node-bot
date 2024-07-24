from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler
import logging
from textwrap import dedent

import constants as const
import mixnet_query as mx_query
import data
import telegram_utils as tgu


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
    job_queue.run_repeating(report_nodes, interval=const.INTERVAL)

    application.run_polling()


async def add_mixnode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not tgu.authorized(update.effective_chat.id):
        id = update.effective_chat.id
        await tgu.send_message(context, "Unauthorized chat", id)
        return

    updated = await increment_list(MIXNODES, context.args, 'mixnode', context)

    if updated:
        try:
            data.update_mixnodes(MIXNODES)
        except Exception as e:
            msg = f'Failed to update mixnodes file:\n\n{e}'
            await tgu.send_message(context, msg)


async def del_mixnode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not tgu.authorized(update.effective_chat.id):
        id = update.effective_chat.id
        await tgu.send_message(context, "Unauthorized chat", id)
        return

    updated = await reduce_list(MIXNODES, context.args, "mixnode", context)

    if updated:
        try:
            data.update_mixnodes(MIXNODES)
        except Exception as e:
            msg = f'Failed to update mixnodes file:\n\n{e}'
            await tgu.send_message(context, msg)


async def add_gateway(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not tgu.authorized(update.effective_chat.id):
        id = update.effective_chat.id
        await tgu.send_message(context, "Unauthorized chat", id)
        return

    updated = await increment_list(GATEWAYS, context.args, 'gateway', context)

    if updated:
        try:
            data.update_gateways(GATEWAYS)
        except Exception as e:
            msg = f'Failed to update gateways file:\n\n{e}'
            await tgu.send_message(context, msg)


async def del_gateway(updated: Update, context: ContextTypes.DEFAULT_TYPE):
    if not tgu.authorized(updated.effective_chat.id):
        id = updated.effective_chat.id
        await tgu.send_message(context, "Unauthorized chat", id)
        return

    updated = await reduce_list(GATEWAYS, context.args, "gateway", context)

    if updated:
        try:
            data.update_gateways(GATEWAYS)
        except Exception as e:
            msg = f'Failed to update gateways file:\n\n{e}'
            await tgu.send_message(context, msg)


async def report_nodes(context: ContextTypes.DEFAULT_TYPE):
    for mixnode in MIXNODES:
        score = mx_query.get_node_score(mixnode, 'mixnode')
        if score < const.MIN_SCORE:
            msg = f"""
                Mixnode {mixnode} having issues, current routing score: {score}
                \nExplorer: {const.MIXNODE_EXPLORER}{mixnode}
                """
            await tgu.send_message(context, dedent(msg))

    for gateway in GATEWAYS:
        score = mx_query.get_node_score(gateway, 'gateway')
        if score < const.MIN_SCORE:
            msg = f"""
                Gateway {gateway} having issues, current routing score: {score}
                \nExplorer: {const.GATEWAY_EXPLORER}{gateway}
                """
            await tgu.send_message(context, dedent(msg))


async def increment_list(watchlist, nodes, node_type, context):
    incremented = False
    for node in nodes:
        if mx_query.node_exists(node, node_type):
            watchlist.append(node)
            msg = f'Added {node_type} {node} to watchlist'
            incremented = True
        else:
            msg = f'Error: {node_type} {node} 404 or API is not reachable'
        await tgu.send_message(context, msg)
    return incremented


async def reduce_list(watchlist, nodes, node_type, context):
    reduced = False
    for node in nodes:
        try:
            watchlist.remove(node)
            msg = f'Removed {node_type} {node}'
            reduced = True
            await tgu.send_message(context, msg)
        except Exception:
            pass
    return reduced


if __name__ == '__main__':
    main()
