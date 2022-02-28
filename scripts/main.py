from BotFuncs import *
import telebot
import json 
from config import BOT_CONFIG


TOKEN = BOT_CONFIG['API_TOKEN']

PLOTS_KEYBOARD_MARKUP = generate_keyboard('plots_keyboard')
DATE_FILTER_KEYBOARD_MARKUP = generate_keyboard('date_filter_keyboard')
CUSTOM_DATE_INLINE_KEYBOARD_MARKUP = generate_inline_keyboard('add_spending_set_custom_date')

BOT = telebot.TeleBot(token=TOKEN)

USER_INSERTS = {}
CUSTOM_DATE = {}


def clear_user_insert(user_id):
    global USER_INSERTS
    
    if user_id in USER_INSERTS:
        USER_INSERTS[user_id] = None


def user_has_insert(user_id):
    global USER_INSERTS
    
    return bool(USER_INSERTS[user_id]) if user_id in USER_INSERTS else False
   
    
def handle_insertion_input(message):
    insertion_dict = parse_message_to_insert_dict(message)
    USER_INSERTS[message.from_user_id] = insertion_dict
    
    BOT.send_message(message.chat.id, 'На какую дату записать затрату?' reply_markup=CUSTOM_DATE_INLINE_KEYBOARD_MARKUP)


@BOT.message_handler(commands=["add_spending"])
def handle_add_spending(message):
    sent = send_reply_text_by_command(BOT, message.chat.id, 'add_spending')
    BOT.register_next_step_handler(sent, handle_insertion_input)
    
    


while True:
    BOT.polling(none_stop=True)