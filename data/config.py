import os
from dotenv import load_dotenv

load_dotenv('.env')
load_dotenv('../.env')   # todo: remove. Put here to enable running/testing
                                # middleware and scraper from their folders
BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

admins = [os.getenv('ADMIN_ID')]

ip = os.getenv('BOT_IP')

IRONSTAR_EVENT_LIST_URL = str(os.getenv('IRONSTAR_EVENT_LIST_URL'))
IRONSTAR_BASE_URL = str(os.getenv('IRONSTAR_BASE_URL'))
