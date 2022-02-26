import telebot
import json 
from config import BOT_CONFIG

TOKEN = BOT_CONFIG['API_TOKEN']

BOT = telebot.TeleBot(token=TOKEN)


while True:
    BOT.polling(none_stop=True)