from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils import helpers

test_keyboard = [['top-left', 'top-right'],
                   ['bottom-left', 'bottom-right']]
reply_markup = ReplyKeyboardMarkup(test_keyboard)


test_inline_keyboard = [
    [
        InlineKeyboardButton("Option 1", callback_data='1'),
        InlineKeyboardButton("Option 2", callback_data='2'),
    ],
    [InlineKeyboardButton("Option 3", callback_data='3')],
]

reply_inline_test_markup = InlineKeyboardMarkup(test_inline_keyboard)


def make_single_button_kbd(key_name, key_payload):
    return InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(key_name, key_payload)
    )


def prepare_pin_message_kbd(bot, destination):
    url = helpers.create_deep_linked_url(bot_username=bot.get_me().username, payload=destination)
    return make_single_button_kbd('start', url)


def keyboard_maker(keys: list):
    def recursive_map(f, lst):
        return (list(recursive_map(f, x) if isinstance(x, list) else f(x) for x in lst))

    result = recursive_map(lambda k: InlineKeyboardButton(k, callback_data=k), keys)
    return InlineKeyboardMarkup(result)
    # def convert_key_to_markup(k):
    #     return InlineKeyboardButton(k, callback_data=key)


# test code
l = [['b1','b2'], ['b3']]
reply_inline_test_markup = InlineKeyboardMarkup(keyboard_maker(l))
