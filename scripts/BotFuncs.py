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


def save_user_insertion(user_id, user_inserts_dict, db_connection):
    if user_inserts_dict[user_id]:
        user_insertion_dict = user_inserts_dict[user_id]
        insert_user_spending(user_insertion_dict, db_connection)
        return 'Успешно сохранил затрату в базу данных!'
    return 'Ошибка! не нашёл запись затраты'


def delete_user_insertion(user_id, user_inserts_dict):
    if user_id in user_inserts_dict:
        del(user_inserts_dict[user_id])
    return 'Отменил запись затраты. Чтобы снова ввести затрату, напишите /add_spending'


def rename_category(user_id, cat_before, cat_after, db_connection):

    try:
        update_category_query = generate_update_query('spendings', {'category': cat_after}, {
            'user_id': user_id,
            'category': cat_before
        })
        exec_update_query(db_connection, update_category_query)
        return 'Успешно переименовал категорию'
    except Exception as e:
        return 'Ошибка! Не смог переименовать категорию'

def get_categories_message(user_id, db_connection):
    
    try:
        categories_query = generate_select_query('spendings', ['category'], where={'user_id': user_id}, distinct=True)


        user_categories = exec_select_query(db_connection, categories_query)

        user_categories = list(user_categories)
        user_categories = [f'📍{category[0]}' for category in user_categories]

        return '\n'.join(user_categories)

    except Exception as e:  
        print('get_categories_message ->', e)
        return 'Ошибка! Не смог найти категории затрат'


def delete_all_user_inserts(user_id, db_connection):

    try:
        delete_user_inserts_query = generate_delete_query('spendings', {'user_id': user_id})
        print(delete_user_inserts_query)
        exec_delete_query(db_connection, delete_user_inserts_query)
        return 'Успешно удалил все записи'
    except Exception as e:
        print('delete_all_user_inserts -> ', e)
        return f'Ошибка! Не смог удалить все записи'


