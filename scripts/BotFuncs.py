from scripts.ParseMessages import parse_message_to_insert_dict
import telebot
import LoadData as ld
import DbFuncs as dbf
import DataFrames as dfr
import plots as plts
from config import BOT_CONFIG


def generate_keyboard(json_key: str):
    global BOT_CONFIG    
    
    KEYBOARD_BUTTONS_JSON_FILEPATH = BOT_CONFIG['KEYBOARD_BUTTONS_JSON_FILEPATH']
    
    try:
        keyboards_json = ld.load_json(KEYBOARD_BUTTONS_JSON_FILEPATH)
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
        keyboards_json = ld.load_json(INLINE_KEYBOARD_BUTTONS_JSON)
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
        dbf.insert_user_spending(user_insertion_dict, db_connection)
        return 'Успешно сохранил затрату в базу данных!'
    return 'Ошибка! не нашёл запись затраты'


def delete_user_insertion(user_id, user_inserts_dict):
    if user_id in user_inserts_dict:
        del(user_inserts_dict[user_id])
    return 'Отменил запись затраты. Чтобы снова ввести затрату, напишите /add_spending'


def rename_category(user_id, cat_before, cat_after, db_connection):

    try:
        update_category_query = dbf.generate_update_query('spendings', {'category': cat_after}, {
            'user_id': user_id,
            'category': cat_before
        })
        dbf.exec_update_query(db_connection, update_category_query)
        return 'Успешно переименовал категорию'
    except Exception as e:
        return 'Ошибка! Не смог переименовать категорию'


def get_categories_message(user_id, db_connection):
    
    try:
        categories_query = dbf.generate_select_query('spendings', ['category'], where={'user_id': user_id}, distinct=True)

        user_categories = dbf.exec_select_query(db_connection, categories_query)

        user_categories = list(user_categories)
        user_categories = [f'📍{category[0]}' for category in user_categories]

        return '\n'.join(user_categories)

    except Exception as e:  
        print('get_categories_message ->', e)
        return 'Ошибка! Не смог найти категории затрат'


def delete_all_user_inserts(user_id, db_connection):

    try:
        delete_user_inserts_query = dbf.generate_delete_query('spendings', {'user_id': user_id})
        print(delete_user_inserts_query)
        dbf.exec_delete_query(db_connection, delete_user_inserts_query)
        return 'Успешно удалил все записи'
    except Exception as e:
        print('delete_all_user_inserts -> ', e)
        return f'Ошибка! Не смог удалить все записи'


def get_user_plot(user_id: str, user_plot_type: str, user_plot_date: str, db_connection):

    user_plot_type = user_plot_type.replace('plot_type_', '')
    user_plot_date = user_plot_date.replace('plot_date_', '')

    user_spendings_query = dbf.generate_select_query('spendings', '*', where={'user_id': user_id})
    user_spendings_rows = dbf.exec_select_query(db_connection, user_spendings_query)

    user_spendings_df = dfr.load_df_from_db_rows(user_spendings_rows)
    #user_spendings_df = eval(f'dfr.filter_{user_plot_date}(user_spendings_df)')
    print(user_spendings_df['date'].dtype)

    user_plot_filepath = plts.generate_plot_filepath(user_id, user_plot_type, user_plot_date)

    if ld.img_exists(user_plot_filepath):
        return user_plot_filepath

    return eval(f'plts.{user_plot_type}(user_spendings_df, user_plot_date)')

