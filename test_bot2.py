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

LEFT, RIGHT = map(chr, range(1, 3))
UP, DOWN = map(chr, range(3, 5))
SELECTING_WAY, SELECTING_UP_DOWN = map(chr, range(20, 22))
STOPPING, RESTART = map(chr, range(99, 101))
END = ConversationHandler.END

def start(update : Update, context: CallbackContext):
    text = 'First level selection: left or right'
    buttons= [
        [
            InlineKeyboardButton(text='left', callback_data=str(LEFT)),
            InlineKeyboardButton(text='right', callback_data=str(RIGHT))
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text=text, reply_markup=keyboard)
    return SELECTING_WAY

def left(update : Update, context: CallbackContext):
    text = 'Second level selection on left side: up or down?'
    buttons = [
        [
            InlineKeyboardButton(text='up', callback_data=str(UP)),
            InlineKeyboardButton(text='down', callback_data=str(DOWN))
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return SELECTING_UP_DOWN

def right(update : Update, context: CallbackContext):
    text = 'Second level selection on right side: up or down?'
    buttons = [
        [
            InlineKeyboardButton(text='up', callback_data=str(UP)),
            InlineKeyboardButton(text='down', callback_data=str(DOWN))
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return SELECTING_UP_DOWN

def stop_nested(update: Update, context: CallbackContext) -> None:
    """Completely end conversation from within nested conversation."""
    update.message.reply_text('Okay, bye.')

    return STOPPING

def stop(update : Update, context: CallbackContext):
    update.message.reply_text('Bye.')
    return END

def end(update: Update, context: CallbackContext) -> None:
    """End conversation from InlineKeyboardButton."""
    update.callback_query.answer()

    text = 'See you around!'
    update.callback_query.edit_message_text(text=text)

    return END

def main():

    # Setting-up bot
    updater = MyUpdater(token=config.BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_error_handler(error_handler.error)


    going_left_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(left, pattern='^' + str(LEFT) + '$')],
        states={SELECTING_UP_DOWN: []},
        fallbacks=[CommandHandler('stop', stop_nested),],
        map_to_parent={
            END: SELECTING_WAY,
            STOPPING: END

        }
    )

    going_right_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(right, pattern='^' + str(RIGHT) + '$')],
        states={SELECTING_UP_DOWN: []},
        fallbacks=[
            CommandHandler('stop', stop_nested),
        ],
        map_to_parent={
            END: SELECTING_WAY,
            STOPPING: END
        }
    )

    main_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_WAY: [
                going_left_conv,
                going_right_conv,
                CallbackQueryHandler(end, pattern='^' + str(END) + '$'),
            ],
            RESTART: [CallbackQueryHandler(start, pattern='^' + str(END) + '$')],
            STOPPING: [CommandHandler('start', start)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    dispatcher.add_handler(main_conv_handler)
    updater.start_polling()
    # updater.idle()


if __name__ == '__main__':
    main()
