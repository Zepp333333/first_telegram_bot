from telegram.ext import Updater
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

with open('TOKEN.txt', 'r') as f:
    TOKEN = f.read()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
