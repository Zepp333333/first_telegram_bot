#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]

from telegram.ext import CallbackContext, Updater, InlineQueryHandler
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, CallbackQueryHandler
from telegram import Update

from data import config
from handlers.conv import *
from handlers import error_handler
from cusom_updater import MyUpdater
from data import data_wrapper


def main():
    # Setting-up bot
    updater = MyUpdater(token=config.BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_error_handler(error_handler.error)

    # instantiating and populating the EventList
    event_list = data_wrapper.get_event_list()

    find_team_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(self_role, pattern='^' + str(IN_SEARCH_FOR_TEAM) + '$')],
        states={
            VIEW_OPTIONS: [CallbackQueryHandler(lambda update, context: select_event(update, context, event_list),
                                                pattern=
                                                '^' + str(SWIMMER) + '$|^'
                                                + str(BIKER) + '$|^'
                                                + str(RUNNER) + '$')],
            GOT_SELF_ROLE: [CallbackQueryHandler(lambda update, context: select_event(update, context, event_list),
                                                 pattern=
                                                 '^' + str(SWIMMER) + '$|^'
                                                 + str(BIKER) + '$|^'
                                                 + str(RUNNER) + '$')],
        },
        fallbacks=[
            CallbackQueryHandler(go_back, pattern='^' + str(END) + '$'),
            CommandHandler('stop', stop_nested)
        ],
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
            GOT_SELF_ROLE: [CallbackQueryHandler(start, pattern='^' + str(END) + '$')],
            CHOOSE_ACTION: [find_team_conv, find_athlete_conv],
            # todo show info
            STOPPING: [CommandHandler('start', start)],
        },
        fallbacks=[
            CommandHandler('stop', stop),
            # CommandHandler('start', start),
        ]
    )

    dispatcher.add_handler(main_conv_handler)
    updater.start_polling()
    # updater.idle()


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
