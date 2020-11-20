import telegram


with open('TOKEN.txt', 'r') as f:
    TOKEN = f.read()
bot = telegram.Bot(token=TOKEN)



updates = bot.get_updates()
print([u.message.text for u in updates])



