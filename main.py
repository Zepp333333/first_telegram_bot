import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.utils import helpers

from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, CallbackQueryHandler

from data import config
from cusom_updater import MyUpdater
import filters as filters
import error_handler
import keyboards




logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# State definitions for top level conversation
CHOOSE_ACTION = chr(1)
GATHER_SELF_INFO, GATHER_TARGET_ATHL_INFO = map(chr, range(2, 4))
IN_SEARCH_FOR_TEAM, IN_SEARCH_FOR_ATHLETE = map(chr, range(4, 6))
SWIMMER, BIKER, RUNNER = map(chr, range(15, 18))
GOT_SELF_ROLE = map(chr, range(20, 21))
EVENT_SELECTION = map(chr, range(30, 31))

# State definitions nested conversations
# todo

# Meta States
STOPPING = map(chr, range(99, 100))

# Other Constants
START_OVER = map(chr, range(100, 101))


# Shortcut for ConversationHandler.END
END = ConversationHandler.END


def start(update: Update, context: CallbackContext):
    """Select an action: Search for Team or an Athlete"""
    logger.info("User %s got into /start with command %s",
                update.message.from_user.first_name, update.message.text)
    text = (
        'Привет! Я помогаю найти недостающего атлета '
        'или целую команду для участия в триатлонной эстафете. '
        'Что будем делать?'
    )
    buttons = [
        [
            InlineKeyboardButton(text='Я атлет, хочу найти команду', callback_data=str(IN_SEARCH_FOR_TEAM)),
            InlineKeyboardButton(text='Ищу атлета для команды', callback_data=str(IN_SEARCH_FOR_ATHLETE)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text=text, reply_markup=keyboard)

    # # If we're starting over we don't need do send a new message
    # if context.user_data.get(START_OVER):
    #     update.callback_query.answer()
    #     update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    # else:
    #     update.message.reply_text(
    #         'Hi, I\'m FamiliyBot and here to help you gather information' 'about your family.'
    #     )
    #     update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return CHOOSE_ACTION


def self_role(update: Update, context: CallbackContext):

    logger.info("User %s is searching for a team in %s",
                update.callback_query.from_user.first_name, "self_role")
    context.user_data['goal'] = IN_SEARCH_FOR_TEAM
    text = (
        'Ок, ищем команду.\n '
        'Расскажи о себе. '
    )
    buttons = [
        [
            InlineKeyboardButton(text='Я пловец', callback_data=str(SWIMMER)),
            InlineKeyboardButton(text='Я велосипедист', callback_data=str(BIKER)),
            InlineKeyboardButton(text='Я бегун', callback_data=str(RUNNER)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return GOT_SELF_ROLE



def select_event(update: Update, context: CallbackContext):
    logger.info('User %s got to %s',
                update.callback_query.from_user.first_name, 'select_event')
    context.user_data['role'] = update.callback_query.data

    text = (
        'Ок, ищем команду.\n '
        'Ты ' + str(context.user_data['role']) + '\n'  #Todo - make sure we print user role
        'В какой гонке ты хочешь участовоать?'
    )
    buttons = [
        [
            InlineKeyboardButton(text='Гонка 1', callback_data=str(1)),
            InlineKeyboardButton(text='Гонка 2', callback_data=str(2)),
            InlineKeyboardButton(text='Гонка 3', callback_data=str(3)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

def in_search_for_athlete(update: Update, context: CallbackContext):
    # TODO: STUB
    update.callback_query.edit_message_text('Cool, we\'re in in search for athlete conversation stream')
    return END




def stop(update: Update, context: CallbackContext):
    """End Conversation by command."""
    update.message.reply_text('До встречи!')
    return END

def stop_nested(update: Update, context: CallbackContext) -> None:
    """Completely end conversation from within nested conversation."""
    update.message.reply_text('Okay, bye.')
    return STOPPING

def end(update: Update, context: CallbackContext) -> None:
    """End conversation from InlineKeyboardButton."""
    update.callback_query.answer()
    text = 'До встречи!'
    update.callback_query.edit_message_text(text=text)
    return END


def main():

    # Setting-up bot
    updater = MyUpdater(token=config.BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_error_handler(error_handler.error)

    find_team_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(self_role, pattern='^' + str(IN_SEARCH_FOR_TEAM) + '$')],
        states={
            GOT_SELF_ROLE: [CallbackQueryHandler(select_event,
                                                 pattern=
                                                 '^' + str(SWIMMER) + '$|^'
                                                 + str(BIKER) + '$|^'
                                                 + str(RUNNER) + '$')],
        },
        fallbacks=[CommandHandler('stop', stop_nested)],
        map_to_parent={
            END: CHOOSE_ACTION,
            STOPPING: END
        }
    )

    find_athlete_conv = ConversationHandler(
        entry_points=[],
        states={},
        fallbacks=[],
        map_to_parent={
            END: CHOOSE_ACTION,
            STOPPING: END
        }
    )

    # Top level conversation handler
    main_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('Start', start)],
        states={
            CHOOSE_ACTION: [find_team_conv, find_athlete_conv],
            # todo show info
            STOPPING: [CommandHandler('start', start)]
        },
        fallbacks=[CommandHandler('stop', stop)],
    )


    dispatcher.add_handler(main_conv_handler)
    updater.start_polling()
    updater.idle()


'''
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


if __name__ == '__main__':
    main()
