from data import config
import logging
from CusomUpdater import MyUpdater
import CustomFilters as Filters
import ErrorHandler


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# bot = Bot(token=config.BOT_TOKEN)
# bot.get_me()
# updater = MyUpdater(bot=bot)

updater = MyUpdater(token=config.BOT_TOKEN, use_context=True)
updater.dispatcher.add_error_handler(ErrorHandler.error)


@updater.make_command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I'm a bot, please talk to me!")


@updater.make_command
def hello(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi there!")


@updater.make_msg(fltr=Filters.any_text_not_a_command)
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=update.message.text)


@updater.make_msg(fltr=Filters.any_command)
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry. I didn't understand the command.")


# start_handler = CommandHandler('start', start)
# dp.add_handler(start_handler)
updater.start_polling()
# updater.idle()
