import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from middleware.event_list import EventList
from keyboards import PagingKeyboard, make_paging_keyboard



# todo : offload all logging into separate module
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# State definitions for top level conversation
CHOOSE_ACTION = chr(1)
GATHER_SELF_INFO, GATHER_TARGET_ATHL_INFO = map(chr, range(2, 4))
IN_SEARCH_FOR_TEAM, IN_SEARCH_FOR_ATHLETE = map(chr, range(4, 6))
SWIMMER, BIKER, RUNNER = ('swimmer', 'biker', 'runner')

SELECT_SEARCH_OPTION, EVENT_SELECTION = map(chr, range(20, 22))

OPTION_SELECTED = map(chr, range(30, 31))

VIEW_EVENTS, VIEW_REQUESTS = map(chr, range(40, 42))


# State definitions nested conversations
# todo

# Meta States
BACK, STOPPING = map(chr, range(98, 100))

# Other Constants
START_OVER = map(chr, range(100, 101))

# Shortcuts
END = ConversationHandler.END
BACK_KEY = InlineKeyboardButton(text='Назад', callback_data=str(END))

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


def set_athlete_role(update: Update, context: CallbackContext):

    logger.info("User %s is searching for a team in %s",
                update.callback_query.from_user.first_name, "set_athlete_role")
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
        [BACK_KEY]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    context.user_data['level'] = GATHER_SELF_INFO
    print('state=EVENT_SELECTION')
    return SELECT_SEARCH_OPTION
    # return EVENT_SELECTION


def select_view_races_or_requests(update: Update, context: CallbackContext):
    logger.info("User %s is selecting search option",
                update.callback_query.from_user.first_name)
    logger.info('userdata %s', context.user_data)

    context.user_data['role'] = update.callback_query.data
    role = update.callback_query.data
    text = (
        f'Можем выбрать гонку для участия.\n'
        f'Или посмотреть все заявки на поиск {role}. '
    )
    buttons = [
        [
            InlineKeyboardButton(text='Выбрать гонку', callback_data=str(EVENT_SELECTION)),
            InlineKeyboardButton(text='Посмотреть все заявки', callback_data=str(VIEW_REQUESTS)),
        ],
        [BACK_KEY]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    context.user_data['level'] = GATHER_SELF_INFO
    print('state=IN_SEARCH_FOR_TEAM')
    return OPTION_SELECTED

# todo : remove - not needed
def paging_event(update: Update, context: CallbackContext, event_list: EventList):
    logger.info('User %s got to %s',
                update.message.from_user.first_name, 'select_event')
    logger.info('userdata %s', context.user_data)
    static_text = (
            'Ок, ищем команду. '
            'Ты '  + '\n'
                                                                    'В какой гонке ты хочешь участвовать?'
                                                                    '\n'
                                                                    '\n'
    )

    pages = event_list.filtered_page_print(5, print_method='get_text_with_selector')
    page = pages[0]
    total_pages = len(pages)
    keyboard = PagingKeyboard(total_pages)
    update.message.reply_text(text=static_text + page,
                              reply_markup=keyboard.make_keyboard_markup(0),
                              disable_web_page_preview=True)
    context.user_data['last_paging_query'] = ''


def select_event(update: Update, context: CallbackContext, event_list: EventList):
    logger.info('User %s got to %s',
                update.callback_query.from_user.first_name, 'select_event')
    logger.info('userdata %s', context.user_data)

    # context.user_data['role'] = update.callback_query.data
    static_text = (
        'Ок, ищем команду. '
        'Ты ' + translation_dict[(context.user_data['role'])] + '\n'
        'В какой гонке ты хочешь участвовать?'
        '\n'
        '\n'
    )

    pages = event_list.filtered_page_print(5, print_method='get_text_with_selector')
    page = pages[0]
    total_pages = len(pages)
    active_page = 0
    keyboard = make_paging_keyboard(total_pages=total_pages, active_page=active_page, keys_below=[BACK_KEY])
    update.callback_query.edit_message_text(text=static_text + page,
                                            reply_markup=keyboard,
                                            disable_web_page_preview=True)
    context.user_data['last_paging_query'] = ''
    context.user_data['level'] = EVENT_SELECTION
    print('state = VIEW_EVENTS ')
    return VIEW_EVENTS


def paging_callback(update: Update, context: CallbackContext, event_list: EventList):
    query = update.callback_query
    if not query.data == context.user_data['last_paging_query']:
        query.answer()
        page_number = int(query.data.split('#')[1])
        pages = event_list.filtered_page_print(5, print_method='get_text_with_selector')
        total_pages = len(pages)
        page = pages[page_number]
        keyboard = make_paging_keyboard(total_pages=total_pages, active_page=page_number, keys_below=[BACK_KEY])
        query.edit_message_text(text=page, reply_markup=keyboard)
    else:
        query.answer()
    context.user_data['last_paging_query'] = query.data
    return VIEW_EVENTS


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
        set_athlete_role(update, context)
        print('state=IN_SEARCH_FOR_TEAM')
        return EVENT_SELECTION


def stop(update: Update, context: CallbackContext):
    """End Conversation by command."""
    text = (
        'До встречи!'
        '\n'
        'Чтобы начать заново - нажми /start'
    )
    update.message.reply_text(text)
    print('state = END')
    return END


def stop_nested(update: Update, context: CallbackContext) -> None:
    """Completely end conversation from within nested conversation."""
    text = (
        'До встречи!'
        '\n'
        'Чтобы начать заново - нажми /start'
    )
    update.message.reply_text(text)
    print('state = STOPPING')
    return STOPPING


def end(update: Update, context: CallbackContext) -> None:
    """End conversation from InlineKeyboardButton."""
    update.callback_query.answer()
    text = 'До встречи!'
    update.callback_query.edit_message_text(text=text)
    print('state = END')
    return END


