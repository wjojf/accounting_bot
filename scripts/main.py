import telebot
import json 
from config import BOT_CONFIG
import DbFuncs as dbf
import LoadData as ld
import BotFuncs as bf
import ParseMessages as pm

try:
    import Image
except:
    from PIL import Image

TOKEN = BOT_CONFIG['API_TOKEN']


# KEYBOARDS
PLOTS_INLINE_KEYBOARD_MARKUP = bf.generate_inline_keyboard('plots_keyboard')
PLOT_DATE_FILTER_KEYBOARD_MARKUP = bf.generate_inline_keyboard('plot_date_filter_keyboard')
CUSTOM_DATE_INLINE_KEYBOARD_MARKUP = bf.generate_inline_keyboard('add_spending_set_custom_date')
VERIFY_INSERTION_INLINE_KEYBOARD_MARKUP = bf.generate_inline_keyboard('verify_insertion_keyboard')
VERIFY_DELETE_ALL_INLINE_KEYBOARD_MARKUP = bf.generate_inline_keyboard('verify_delete_all')

# BOTS
BOT = telebot.TeleBot(token=TOKEN)


# DB CONNECTION
DB_CONN = dbf.create_conn()


# USER INSERT DICTS
USER_INSERTS = {}
USER_INSERTS_DATE = {}
USER_PLOT_TYPE = {}
USER_PLOT_DATE = {}


def set_user_spending_date(user_id, date):
    global USER_INSERTS_DATE
    USER_INSERTS_DATE[str(user_id)] = date


def set_user_spending_dict(user_id, user_dict):
    global USER_INSERTS
    USER_INSERTS[str(user_id)] = user_dict


def set_user_plot_type(user_id, plot_type):
    global USER_PLOT_TYPE
    USER_PLOT_TYPE[str(user_id)] = plot_type


def set_user_plot_date(user_id, date):
    global USER_PLOT_DATE
    USER_PLOT_DATE[str(user_id)] = date


def clear_user_plot(user_id: str):
    global USER_PLOT_TYPE, USER_PLOT_DATE

    if user_id in USER_PLOT_TYPE:
        del(USER_PLOT_TYPE[user_id])
    if user_id in USER_PLOT_DATE:
        del(USER_PLOT_DATE[user_id])


def handle_current_date_input(message):

    user_id = str(message.chat.id)
    user_date = ld.get_current_date()

    set_user_spending_date(user_id, user_date)

    ask_for_input = ld.load_command_reply_text('ask_for_input')
    ask_for_input_message = BOT.send_message(message.chat.id, ask_for_input)
    BOT.register_next_step_handler(ask_for_input_message, handle_insertion_input)


def handle_custom_date_input(message):

    user_id = str(message.chat.id)
    user_date = message.text

    set_user_spending_date(user_id, user_date)

    ask_for_input = ld.load_command_reply_text('ask_for_input')
    ask_for_input_message = BOT.send_message(message.chat.id, ask_for_input)
    BOT.register_next_step_handler(ask_for_input_message, handle_insertion_input)


def handle_insertion_input(message):
    try:
        user_id = str(message.from_user.id)
        user_date = USER_INSERTS_DATE[user_id]
        insertion_dict = pm.parse_message_to_insert_dict(message.text, user_id, user_date)

        set_user_spending_dict(user_id, insertion_dict)

        validating_message = pm.generate_validating_message(insertion_dict)
        BOT.send_message(message.chat.id, validating_message, reply_markup=VERIFY_INSERTION_INLINE_KEYBOARD_MARKUP)

    except Exception as e:
        print('handle_insertion_input', e)
        BOT.send_message(message.chat.id, 'Ошибка, не смог получить затрату')


def handle_rename_category_message(message):
    try:
        cat_before, cat_after = message.text.split()
        user_id = str(message.from_user.id)
        renaming_result = bf.rename_category(user_id, cat_before, cat_after, DB_CONN)
        BOT.send_message(message.chat.id, renaming_result)

    except Exception as e:
        print('handle_rename_category ->', e)
        categories_failure_text = ld.load_command_reply_text('get_categories_failure')
        BOT.send_message(message.chat.id, categories_failure_text)


def prepare_user_plot(callback):

    user_id = str(callback.message.chat.id)
    user_plot_type = USER_PLOT_TYPE[user_id]
    user_plot_date = USER_PLOT_DATE[user_id]

    user_plot_image_filepath = bf.get_user_plot(user_id, user_plot_type, user_plot_date)
    plot_reply_text = ld.load_command_reply_text('plot_message')
    clear_user_plot(user_id)

    user_plot_image = open(user_plot_image_filepath, 'rb')
    BOT.send_photo(callback.message.chat.id, user_plot_image, caption=plot_reply_text)


@BOT.message_handler(commands=['start', 'help'])
def handle_start(message):
    reply_text = ld.load_command_reply_text('help')
    commands_description = ld.load_commands_description()

    reply_message = reply_text + '\n' + pm.generate_validating_message(commands_description)

    BOT.send_message(message.chat.id, reply_message)


@BOT.message_handler(commands=['add_spending'])
def handle_add_spending(message):
    reply_text = ld.load_command_reply_text('add_spending')
    BOT.send_message(message.chat.id, reply_text, reply_markup=CUSTOM_DATE_INLINE_KEYBOARD_MARKUP)


@BOT.message_handler(commands=['rename_category'])
def handle_rename_category(message):
    rename_category_reply = ld.load_command_reply_text('rename_category')
    sent = BOT.send_message(message.chat.id, rename_category_reply)
    BOT.register_next_step_handler(sent, handle_rename_category_message)


@BOT.message_handler(commands=['show_categories'])
def handle_show_categories(message):
    reply_text = ld.load_command_reply_text('show_categories') + '\n'

    categories_message = bf.get_categories_message(str(message.from_user.id), DB_CONN)

    final_message = reply_text + categories_message

    BOT.send_message(message.chat.id, final_message)


@BOT.message_handler(commands=['delete_all'])
def handle_delete_all(message):
    reply_text = ld.load_command_reply_text('delete_all')
    BOT.send_message(message.chat.id, reply_text, reply_markup=VERIFY_DELETE_ALL_INLINE_KEYBOARD_MARKUP)


@BOT.message_handler(commands=['plots'])
def handle_plots(message):
    reply_text = ld.load_command_reply_text('plots')

    BOT.send_message(message.chat.id, reply_text, reply_markup=PLOTS_INLINE_KEYBOARD_MARKUP)


@BOT.callback_query_handler(func=lambda call: True)
def handle_callback(call):

    callback_data = call.data
    callback_user_id = call.from_user.id
    callback_chat_id = call.message.chat.id
    callback_message = call.message

    if 'spending_date' in call.data:

        if call.data == 'spending_date_today':
            handle_current_date_input(callback_message)

        elif call.data == 'spending_date_custom':
            ask_for_date_input = ld.load_command_reply_text('ask_for_date_input')
            sent = BOT.send_message(callback_chat_id, ask_for_date_input)
            BOT.register_next_step_handler(sent, handle_custom_date_input)

    elif 'verify_insertion' in call.data:
        
        if call.data == 'verify_insertion_true':
            saving_result = bf.save_user_insertion(str(callback_user_id), USER_INSERTS, DB_CONN)
            BOT.send_message(callback_chat_id, saving_result)
        else:
            clear_user_insert_result = bf.delete_user_insertion(str(callback_chat_id), USER_INSERTS)
            BOT.send_message(callback_chat_id, clear_user_insert_result)

    elif 'delete_all' in call.data:

        if call.data == 'delete_all_true':
            delete_all_result = bf.delete_all_user_inserts(callback_chat_id, DB_CONN)
            BOT.send_message(callback_chat_id, delete_all_result)

        elif call.data == 'delete_all_false':
            cancel_delete_text = ld.load_command_reply_text('cancel_delete')
            BOT.send_message(callback_chat_id, cancel_delete_text)

    elif 'plot_type' in call.data:
        set_user_plot_type(callback_chat_id, callback_data)
        ask_for_plot_date_text = ld.load_command_reply_text('ask_for_date_plot_input')
        BOT.send_message(callback_chat_id, ask_for_plot_date_text, reply_markup=PLOT_DATE_FILTER_KEYBOARD_MARKUP)

    elif 'plot_date' in call.data:
        set_user_plot_date(callback_chat_id, callback_data)
        prepare_user_plot(call)


def main():
    BOT.polling(none_stop=True)


if __name__ == '__main__':
    main()