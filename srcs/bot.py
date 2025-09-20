from telegram.ext import Application, ContextTypes, CommandHandler
import logging
from textwrap import dedent

import constants as const
import mixnet_query as mx_query
import data
import telegram_utils as tgu
import handlers as hndlrs


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

try:
    data.NODES = data.load_nodes()
except Exception:
    pass


def main():
    application = Application.builder().token(const.TOKEN).build()

    add_handler = CommandHandler('add', hndlrs.add_node)
    del_handler = CommandHandler('del', hndlrs.del_node)
    sat_handler = CommandHandler('saturation', hndlrs.get_sat)

    application.add_handler(add_handler)
    application.add_handler(del_handler)
    application.add_handler(sat_handler)

    job_queue = application.job_queue
    job_queue.run_repeating(report_nodes, interval=const.INTERVAL)

    application.run_polling()


async def report_nodes(context: ContextTypes.DEFAULT_TYPE):
    for node in data.NODES:
        try:
            score = mx_query.get_node_score(node)
        except Exception as e:
            await tgu.send_message(context, f'Error: {e}')
            continue

        if score < const.MIN_SCORE:
            msg = f"""
                Node {node} having issues, current routing score: {score}
                """
            await tgu.send_message(context, dedent(msg))


if __name__ == '__main__':
    main()
