from scripts.ParseMessages import parse_message_to_insert_dict
import telebot
from telebot.types import InputMediaPhoto
import LoadData as ld
import DbFuncs as dbf
import DataFrames as dfr
import plots as plts
from config import BOT_CONFIG


def generate_keyboard(json_key: str):
    '''
    :param json_key: string key (reference to KeyBoardButtons.json)
    :return: telebot ReplyMarkupKeyboard with texts and callbacks from json file
    '''

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
    '''
    :param json_key:  string key (reference to InlineKeyboardButtons.json)
    :return:  telebot InlineKeyboardMarkup with texts and callbacks from json file
    '''

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
    '''
    :param user_id: string of user telegram id
    :param user_inserts_dict:  user insert in needed format to insert into db
    :param db_connection:  db_connection to insert values
    :return: string: saving result
    '''

    if user_inserts_dict[user_id]:
        user_insertion_dict = user_inserts_dict[user_id]
        dbf.insert_user_spending(user_insertion_dict, db_connection)
        return 'Успешно сохранил затрату в базу данных!'
    return 'Ошибка! не нашёл запись затраты'


def delete_user_insertion(user_id, user_inserts_dict):
    '''
    clears user stack of inserts
    :param user_id: string user telegram id
    :param user_inserts_dict: dict of user spendings in needed format
    :return: deleting results from dict
    '''

    if user_id in user_inserts_dict:
        del(user_inserts_dict[user_id])
    return 'Отменил запись затраты. Чтобы снова ввести затрату, напишите /add_spending'


def rename_category(user_id, cat_before, cat_after, db_connection):

    '''
    renames category for user

    :param user_id: string user telegram id
    :param cat_before: category title before renaming
    :param cat_after:  category title after renaming
    :param db_connection: database connection
    :return:
    '''

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

    '''

    :param user_id: string user telegram id
    :param db_connection: database connection
    :return:  Optional: list of user catgories message / error message
    '''


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

    '''
    Deletes all user inserts from db
    :param user_id: string user telegram id
    :param db_connection: database connection
    :return:
    '''

    try:
        delete_user_inserts_query = dbf.generate_delete_query('spendings', {'user_id': user_id})
        print(delete_user_inserts_query)
        dbf.exec_delete_query(db_connection, delete_user_inserts_query)
        return 'Успешно удалил все записи'
    except Exception as e:
        print('delete_all_user_inserts -> ', e)
        return f'Ошибка! Не смог удалить все записи'


def get_user_plot(user_id: str, user_plot_type: str, user_plot_date: str, db_connection):

    '''
    generates needed plot image and returns its filepath

    :param user_id: string telegram id
    :param user_plot_type: string of plot type in needed format (reference plots.py)
    :param user_plot_date: string of plot date filter in needed format (reference DataFrames.py)
    :param db_connection: database_connection
    :return: user plot filepath
    '''

    user_plot_type = user_plot_type.replace('plot_type_', '')
    user_plot_date = user_plot_date.replace('plot_date_', '')

    user_spendings_query = dbf.generate_select_query('spendings', '*', where={'user_id': user_id})
    user_spendings_rows = dbf.exec_select_query(db_connection, user_spendings_query)

    user_spendings_df = dfr.parse_date_for_df(dfr.load_df_from_db_rows(user_spendings_rows))
    user_spendings_df = eval(f'dfr.filter_{user_plot_date}(user_spendings_df)')
    user_spendings_df = dfr.date_to_str_for_df(user_spendings_df)

    if len(user_spendings_df) > 0:
        return eval(f'plts.{user_plot_type}(user_spendings_df, user_plot_date)')

    return BOT_CONFIG['ERROR_IMAGE_FILEPATH']


def send_plots(BOT, chat_id, user_plots_filepath_list):
    try:

        plot_reply_text = ld.load_command_reply_text('plot_message')
        plot_error_text = ld.load_command_reply_text('plot_error')

        if isinstance(user_plots_filepath_list, list) and len(user_plots_filepath_list) > 1:
            media_group_to_send = []
            opened_images = []

            for plot_filepath in user_plots_filepath_list:
                image = open(plot_filepath, 'rb')
                input_media_photo = InputMediaPhoto(image)
                media_group_to_send.append(input_media_photo)
                opened_images.append(image)

            BOT.send_media_group(chat_id, media_group_to_send)
            BOT.send_message(chat_id, plot_reply_text)

            for opened_image in opened_images:
                opened_image.close()

            for plot_filepath in user_plots_filepath_list:
                ld.delete_image(plot_filepath)

        elif isinstance(user_plots_filepath_list, str):
            if user_plots_filepath_list == BOT_CONFIG['ERROR_IMAGE_FILEPATH']:
                error_image = open(user_plots_filepath_list, 'rb')
                BOT.send_photo(chat_id, error_image, caption=plot_error_text)
            else:
                plot_image = open(user_plots_filepath_list, 'rb')
                BOT.send_photo(plot_image, caption=plot_reply_text)

        return

    except Exception as e:
        print(e)
        return
