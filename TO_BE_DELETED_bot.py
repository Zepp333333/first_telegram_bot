from uuid import uuid4
import telegram.ext
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from data import config


ADMINS = config.admins

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I'm a bot, please talk to me!")


# def echo(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id,
#                              text=update.message.text)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text_caps)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry. I didn't understand the command.")


def callback_minute(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id='199228168',
                             text="One message every minute")


def put(update, context):
    """Usage: /put value"""
    # Generate ID and separate value from command:
    key = str(uuid4())
    # We don't use context.args here because the value may contain whitespaces
    value = update.message.text.partition(' ')[2]

    # Store value
    context.user_data[key] = value
    update.message.reply_text(key)


def get(update, context):
    """Usage: /get uuid"""
    # Separate ID from command
    key = context.args[0]

    # Load value
    value = context.user_data.get(key, 'Not found')
    update.message.reply_text(value)


if __name__ == '__main__':
    # with open('TOKEN.txt', 'r') as f:
    #     TOKEN = f.read()

    # Getting configuration:

    updater = Updater(token=config.BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    # j = updater.job_queue

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    caps_handler = CommandHandler('caps', caps)
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(start_handler)
#    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(caps_handler)
    dispatcher.add_handler(CommandHandler('put', put))
    dispatcher.add_handler(CommandHandler('get', get))
    # Unknown handler should always be last
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
    # job_minute = j.run_repeating(callback_minute, interval=60, first=1)
    updater.idle()
