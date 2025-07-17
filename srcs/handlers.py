from telegram import Update
from telegram.ext import ContextTypes

import mixnet_query as mx_query
import data
import telegram_utils as tgu


async def add_node(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not tgu.authorized(update.effective_chat.id):
        id = update.effective_chat.id
        await tgu.send_message(context, "Unauthorized chat", id)
        return

    updated = await increment_set(data.NODES, context.args, context)

    if updated:
        try:
            data.update_nodes(data.NODES)
        except Exception as e:
            msg = f'Failed to update gateways file:\n\n{e}'
            await tgu.send_message(context, msg)


async def del_node(updated: Update, context: ContextTypes.DEFAULT_TYPE):
    if not tgu.authorized(updated.effective_chat.id):
        id = updated.effective_chat.id
        await tgu.send_message(context, "Unauthorized chat", id)
        return

    updated = await reduce_set(data.NODES, context.args, context)

    if updated:
        try:
            data.update_nodes(data.NODES)
        except Exception as e:
            msg = f'Failed to update gateways file:\n\n{e}'
            await tgu.send_message(context, msg)


async def increment_set(watchlist: set, nodes: list, context):
    incremented = False
    for node in nodes:
        if mx_query.node_exists(node):
            watchlist.add(node)
            msg = f'Added node {node} to watchlist'
            incremented = True
        else:
            msg = f"Error: node {node} 404'd or API is not reachable"
        await tgu.send_message(context, msg)
    return incremented


async def reduce_set(watchlist: set, nodes: list, context):
    reduced = False
    for node in nodes:
        try:
            watchlist.add(node)
            msg = f'Removed node {node}'
            reduced = True
            await tgu.send_message(context, msg)
        except Exception:
            pass
    return reduced
