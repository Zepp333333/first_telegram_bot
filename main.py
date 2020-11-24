from data import config
import logging
from CusomUpdater import MyUpdater
import CustomFilters as Filters
import ErrorHandler

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
def start(update, context):
    print(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I'm a bot, please talk to me!")


@updater.make_command
def hello(update, context):
    print(update)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi there!")

@updater.make_msg(fltr=Filters.help_cmd)
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='help response')

@updater.make_msg(fltr=Filters.any_text_not_a_command)
def echo(update, context):
    print(update.effective_chat['type'])
    if update.effective_chat['type'] == 'channel':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=update.channel_post.text)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=update.effective_message.text)



def hlp(update, context):
    update.message.reply_text('help response')

updater.dispatcher.add_handler(CommandHandler("help", hlp))

@updater.make_msg(fltr=Filters.any_command)
def unknown(update, context):
    print(update)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry. I didn't understand the command.")


# start_handler = CommandHandler('start', start)
# dp.add_handler(start_handler)
updater.start_polling()
# updater.idle()
