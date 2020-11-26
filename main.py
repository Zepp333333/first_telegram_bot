import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.utils import helpers


from data import config
from cusom_updater import MyUpdater
import filters as filters
import error_handler
import keyboards

from telegram.ext import CommandHandler, Filters

GO_PRIVATE = 'go-private'


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# bot = Bot(token=config.BOT_TOKEN)
# bot.get_me()
# updater = MyUpdater(bot=bot)

updater = MyUpdater(token=config.BOT_TOKEN, use_context=True)
updater.dispatcher.add_error_handler(error_handler.error)

@updater.make_command_filter(Filters.regex(GO_PRIVATE))
def start(update: Update, context: CallbackContext):
    bot = context.bot
    url = helpers.create_deep_linked_url(bot.get_me().username, GO_PRIVATE)
    text = "Nice, let's really go private"
    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text='Continue', url=url)
    )
    update.message.reply_text(text, reply_markup=keyboard)


@updater.make_command
def start(update: Update, context: CallbackContext):
    print('start', update)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I'm a bot, please talk to me!")


def send_pin_message(bot_, chat_id, text, destination):
    keyboard = keyboards.prepare_pin_message_kbd(bot_, destination)
    updater.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)


'''
@updater.make_command
def hello(update: Update, context: CallbackContext):
    update.message.reply_text(text="Hi there!")


# @updater.make_command
# def priv(update: Update, context: CallbackContext):
#     print(update.effective_user.id)
#     context.bot.send_message(chat_id=update.effective_user.id, text="priv_response")


@updater.make_msg(fltr=filters.help_cmd)
def help(update: Update, context: CallbackContext):
        update.message.reply_text('Please choose:',
                                  reply_markup=keyboards.reply_inline_test_markup, reply_to_message_id=update.message.message_id)


@updater.make_button
def button(update: Update, context: CallbackContext):
    print('button', update)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected option: {query.data}", reply_markup=keyboards.reply_inline_test_markup)


@updater.make_msg(fltr=filters.any_text_not_a_command)
def echo(update: Update, context: CallbackContext):
    update.message.reply_text(text=update.effective_message.text)


@updater.make_msg(fltr=filters.any_command)
def unknown(update: Update, context: CallbackContext):
    print('unknown', update)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry. I didn't understand the command.")
'''


# updater.dispatcher.add_handler(CommandHandler(command="priv",
#                                               callback=priv,
#                                               filters=Filters.regex(GO_PRIVATE)))

updater.start_polling()
# updater.idle()
