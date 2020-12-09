import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from middleware.event_list import EventList


# todo : offload all logging into separate module
from telegram.utils.helpers import escape_markdown

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# State definitions for top level conversation
CHOOSE_ACTION = chr(1)
GATHER_SELF_INFO, GATHER_TARGET_ATHL_INFO = map(chr, range(2, 4))
IN_SEARCH_FOR_TEAM, IN_SEARCH_FOR_ATHLETE = map(chr, range(4, 6))
SWIMMER, BIKER, RUNNER = ('swimmer', 'biker', 'runner')
GOT_SELF_ROLE = map(chr, range(20, 21))
EVENT_SELECTION = map(chr, range(30, 31))
VIEW_OPTIONS = map(chr, range(40, 41))


# State definitions nested conversations
# todo

# Meta States
BACK, STOPPING = map(chr, range(98, 100))

# Other Constants
START_OVER = map(chr, range(100, 101))

# Shortcut for ConversationHandler.END
END = ConversationHandler.END

translation_dict = {
    'swimmer': 'пловец 🏊',
    'biker': 'велосипедист 🚴',
    'runner': 'бегун 🏃',
}


def start(update: Update, context: CallbackContext):
    """Select an action: Search for Team or an Athlete"""

    text = (
        'Привет! Я бот - помогаю найти недостающего атлета '
        'или целую команду для участия в триатлонной эстафете. \n'
        'Чтобы прекратить это безобразие в любой момент нажми /stop \n '
        'Что будем делать?'
    )
    buttons = [
        [
            InlineKeyboardButton(text='Я атлет, хочу найти команду', callback_data=str(IN_SEARCH_FOR_TEAM)),
            InlineKeyboardButton(text='Ищу атлета для команды', callback_data=str(IN_SEARCH_FOR_ATHLETE)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # If we're starting over we don't need do send a new message
    if context.user_data.get(START_OVER):
        user = update.callback_query.from_user
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        user = update.message.from_user
        update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False

    logger.info('User %s got into /start with command', user)
    logger.info('userdata %s', context.user_data)
    print('state=CHOOSE_ACTION')
    return CHOOSE_ACTION


def self_role(update: Update, context: CallbackContext):

    logger.info("User %s is searching for a team in %s",
                update.callback_query.from_user.first_name, "self_role")
    logger.info('userdata %s', context.user_data)

    context.user_data['goal'] = IN_SEARCH_FOR_TEAM
    text = (
        'Ок, ищем команду.\n'
        'Расскажи о себе. '
    )
    buttons = [
        [
            InlineKeyboardButton(text='Я пловец', callback_data=str(SWIMMER)),
            InlineKeyboardButton(text='Я велосипедист', callback_data=str(BIKER)),
            InlineKeyboardButton(text='Я бегун', callback_data=str(RUNNER)),
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=str(END)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    context.user_data['level'] = GATHER_SELF_INFO
    print('state=GOT_SELF_ROLE')
    return GOT_SELF_ROLE


def select_event(update: Update, context: CallbackContext, event_list: EventList):
    logger.info('User %s got to %s',
                update.callback_query.from_user.first_name, 'select_event')
    logger.info('userdata %s', context.user_data)

    context.user_data['role'] = update.callback_query.data

    static_text = (
        'Ок, ищем команду. '
        'Ты ' + translation_dict[(context.user_data['role'])] + '\n'
        'В какой гонке ты хочешь участвовать?'
        '\n'
        '\n'
    )

    # todo: add paging
    variable_text = '\n'.join(event_list.filtered_page_print(5, 'get_text_with_selector')[0])
    buttons = [
        [
            InlineKeyboardButton(text='Назад', callback_data=str(END)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text=static_text + variable_text,
                                            reply_markup=keyboard,
                                            disable_web_page_preview=True)
    context.user_data['level'] = EVENT_SELECTION
    print('state = VIEW_OPTIONS ')
    return VIEW_OPTIONS


# todo : remove
def select_event_old(update: Update, context: CallbackContext):


    logger.info('User %s got to %s',
                update.callback_query.from_user.first_name, 'select_event')
    logger.info('userdata %s', context.user_data)

    context.user_data['role'] = update.callback_query.data

    text = (
        'Ок, ищем команду.\n'
        'Ты ' + translation_dict[(context.user_data['role'])] + '\n'
        'В какой гонке ты хочешь участовоать?'
    )
    # buttons = [
    #     [
    #         InlineKeyboardButton(text='Гонка 1', callback_data=str(1)),
    #         InlineKeyboardButton(text='Гонка 2', callback_data=str(2)),
    #         InlineKeyboardButton(text='Гонка 3', callback_data=str(3)),
    #     ],
    #     [
    #         InlineKeyboardButton(text='Назад', callback_data=str(END)),
    #     ]
    # ]
    # keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text=text)  #, reply_markup=keyboard)
    context.user_data['level'] = EVENT_SELECTION
    print('state = VIEW_OPTIONS ')
    return VIEW_OPTIONS


def in_search_for_athlete(update: Update, context: CallbackContext):
    # TODO: STUB
    update.callback_query.edit_message_text('Cool, we\'re in in search for athlete conversation stream')
    return END


def go_back(update: Update, context: CallbackContext):
    logger.info('User %s got to %s',
                update.callback_query.from_user.first_name, 'go_back')
    logger.info('userdata %s', context.user_data)

    level = context.user_data['level']
    if level == GATHER_SELF_INFO:
        context.user_data[START_OVER] = True
        start(update, context)
        print('state=END')
        return END
    elif level == EVENT_SELECTION:
        self_role(update, context)
        print('state=IN_SEARCH_FOR_TEAM')
        return GOT_SELF_ROLE


def stop(update: Update, context: CallbackContext):
    """End Conversation by command."""
    update.message.reply_text('До встречи!')
    print('state = END')
    return END


def stop_nested(update: Update, context: CallbackContext) -> None:
    """Completely end conversation from within nested conversation."""
    update.message.reply_text('Okay, bye.')
    print('state = STOPPING')
    return STOPPING


def end(update: Update, context: CallbackContext) -> None:
    """End conversation from InlineKeyboardButton."""
    update.callback_query.answer()
    text = 'До встречи!'
    update.callback_query.edit_message_text(text=text)
    print('state = END')
    return END


