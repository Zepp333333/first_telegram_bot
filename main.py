import logging

from telegram import Update
from telegram.ext import CallbackContext

from data import config
from CusomUpdater import MyUpdater
import CustomFilters as Filters
import ErrorHandler
import Keyboards

# temp/test imports
from telegram.ext import CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# bot = Bot(token=config.BOT_TOKEN)
# bot.get_me()
# updater = MyUpdater(bot=bot)

updater = MyUpdater(token=config.BOT_TOKEN, use_context=True)
updater.dispatcher.add_error_handler(ErrorHandler.error)


@updater.make_command
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I'm a bot, please talk to me!")


@updater.make_command
def hello(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi there!")


@updater.make_msg(fltr=Filters.help_cmd)
def help(update: Update, context: CallbackContext):
    update.message.reply_text('Please choose:', reply_markup=Keyboards.reply_inline_test_markup)

    # context.bot.send_message(chat_id=update.effective_chat.id,
    #                          text='Custom Keyboard Test',
    #                          reply_markup=Keyboards.reply_markup)
    # context.bot.send_message(chat_id=update.effective_chat.id,
    #                              text='help response')


@updater.make_button
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected option: {query.data}", reply_markup=Keyboards.reply_inline_test_markup)


@updater.make_msg(fltr=Filters.any_text_not_a_command)
def echo(update: Update, context: CallbackContext):
    if update.effective_chat['type'] == 'channel':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=update.channel_post.text)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=update.effective_message.text)


@updater.make_msg(fltr=Filters.any_command)
def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry. I didn't understand the command.")


# start_handler = CommandHandler('start', start)
# dp.add_handler(start_handler)
updater.start_polling()
# updater.idle()
