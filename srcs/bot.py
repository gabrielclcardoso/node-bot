from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler
import logging

import constants as const


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    application = Application.builder().token(const.TOKEN).build()

    hello_handler = CommandHandler('hello', hello)
    application.add_handler(hello_handler)

    application.run_polling()


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Hello World!")

if __name__ == '__main__':
    main()
