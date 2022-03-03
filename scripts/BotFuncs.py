from scripts.ParseMessages import parse_message_to_insert_dict
import telebot
from LoadData import *
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

