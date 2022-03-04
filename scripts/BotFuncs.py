from scripts.ParseMessages import parse_message_to_insert_dict
import telebot
from LoadData import *
from DbFuncs import *
from config import BOT_CONFIG


def generate_keyboard(json_key: str):
    global BOT_CONFIG    
    
    KEYBOARD_BUTTONS_JSON_FILEPATH = BOT_CONFIG['KEYBOARD_BUTTONS_JSON_FILEPATH']
    
    try:
        keyboards_json = load_json(KEYBOARD_BUTTONS_JSON_FILEPATH)
        buttons_to_add = keyboards_json[json_key]
    except Exception as e:
        print(e)
        return 
    
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    for button in buttons_to_add:
        button_text, button_callback_data = button['text'], button['callback_data']
        bot_button = telebot.types.KeyboardButton(text=button_text, callback_data=button_callback_data)
        
        keyboard.add(bot_button)
    
    return keyboard

    
def generate_inline_keyboard(json_key: str):
    global BOT_CONFIG

    INLINE_KEYBOARD_BUTTONS_JSON = BOT_CONFIG['INLINE_KEYBOARD_BUTTONS_JSON_FILEPATH']
    
    try:
        keyboards_json = load_json(INLINE_KEYBOARD_BUTTONS_JSON)
        buttons_to_add = keyboards_json[json_key]
    except Exception as e:
        print(e)
        return 
    
    keyboard = telebot.types.InlineKeyboardMarkup()
    
    for button in buttons_to_add:
        button_text, button_callback_data = button['text'], button['callback_data']
        bot_button = telebot.types.InlineKeyboardButton(text=button_text, callback_data=button_callback_data)
        
        keyboard.add(bot_button)
    
    return keyboard


def clear_user_insert(user_id, USER_INSERTS):
    if user_id in USER_INSERTS:
        USER_INSERTS[user_id] = None


def user_has_insert(user_id, USER_INSERTS):
    return bool(USER_INSERTS[user_id]) if user_id in USER_INSERTS else False


def user_has_date(user_id, CUSTOM_DATE):
    return user_id in CUSTOM_DATE


def set_user_spending_date(user_id, CUSTOM_DATE, date):
    CUSTOM_DATE[user_id] = date


def load_user_spending_date(user_id, CUSTOM_DATE):
    return CUSTOM_DATE[user_id]


def save_user_insertion(user_id, USER_INSERTS):
    if user_has_insert(user_id):
        user_insert = USER_INSERTS[user_id]
        insert_user_spending(user_insert)
