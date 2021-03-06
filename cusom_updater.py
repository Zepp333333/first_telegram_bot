from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import Update


# class MyUpdater(Updater):
#     def make_command(self, callback, *args, **kwargs):
#         handler = CommandHandler(callback.__name__,
#                                  callback=callback,
#                                  **kwargs)
#         self.dispatcher.add_handler(handler)
#         print(f"[HANDLER] Add '{callback.__name__}' as a Command Handler")
#         return handler

class MyUpdater(Updater):
    def make_command(self, callback):
        handler = CommandHandler(callback.__name__, callback=callback)
        self.dispatcher.add_handler(handler)
        print(f"[HANDLER] Add '{callback.__name__}' as a Command Handler")
        return handler

    def make_msg(self, fltr):
        def decorator_f(callback):
            handler = MessageHandler(fltr, callback)
            self.dispatcher.add_handler(handler)
            print(f"[HANDLER] Add '{callback.__name__}' as a MessageHandler")
            return handler
        return decorator_f

    def make_command_filter(self, fltr):
        def decorator_f(callback):
            handler = CommandHandler(command=callback.__name__, callback=callback, filters=fltr)
            self.dispatcher.add_handler(handler)
            print(f"[HANDLER] Add '{callback.__name__}' as a CommandHandler with Filter")
            return handler
        return decorator_f

    def make_button(self, callback):
        handler = CallbackQueryHandler(callback=callback)
        self.dispatcher.add_handler(handler)
        print(f"[HANDLER] Add '{callback.__name__}' as a Button Handler")
        return handler


