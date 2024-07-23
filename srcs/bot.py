from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler
import logging

import constants as const


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

JOBS = []


def main():
    application = Application.builder().token(const.TOKEN).build()

    job_handler = CommandHandler('add', add_job)
    application.add_handler(job_handler)

    job_queue = application.job_queue
    job_queue.run_repeating(print_jobs, interval=5)

    application.run_polling()


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
