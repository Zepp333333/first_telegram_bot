from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import Update, bot, message
from telegram.utils import helpers
from keyboards import make_single_button_kbd


def prepare_pin_message_kbd(bot_: bot, destination : str):
    url = helpers.create_deep_linked_url(bot_username=bot_.get_me().username, payload=destination)
    return make_single_button_kbd('start', url)

