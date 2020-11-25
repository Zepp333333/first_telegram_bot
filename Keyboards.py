from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

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
