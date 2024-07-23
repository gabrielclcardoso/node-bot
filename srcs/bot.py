from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler
import logging

import constants as const
import mixnet_query as mx_query


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

JOBS = []


def main():
    application = Application.builder().token(const.TOKEN).build()

    job_handler = CommandHandler('add', add_job)
    mixnode_handler = CommandHandler('mixscore', mixnode_score)
    gateway_handler = CommandHandler('gatescore', gateway_score)

    application.add_handler(job_handler)
    application.add_handler(mixnode_handler)
    application.add_handler(gateway_handler)

    job_queue = application.job_queue
    job_queue.run_repeating(print_jobs, interval=5)

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


async def add_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != const.CHAT_ID:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Unauthorized")

    for job in context.args:
        JOBS.append(job)
        await context.bot.send_message(chat_id=const.CHAT_ID,
                                       text=f'added {job}')


async def print_jobs(context: ContextTypes.DEFAULT_TYPE):
    for job in JOBS:
        await context.bot.send_message(chat_id=const.CHAT_ID, text=job)

if __name__ == '__main__':
    main()
