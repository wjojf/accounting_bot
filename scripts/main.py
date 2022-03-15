import telebot
import json 
from config import BOT_CONFIG
from DbFuncs import create_conn
from BotFuncs import *
from LoadData import *


TOKEN = BOT_CONFIG['API_TOKEN']


# KEYBOARDS
PLOTS_INLINE_KEYBOARD_MARKUP = generate_inline_keyboard('plots_keyboard')
DATE_FILTER_KEYBOARD_MARKUP = generate_inline_keyboard('date_filter_keyboard')
CUSTOM_DATE_INLINE_KEYBOARD_MARKUP = generate_inline_keyboard('add_spending_set_custom_date')
VERIFY_INSERTION_INLINE_KEYBOARD_MARKUP = generate_inline_keyboard('verify_insertion_keyboard')
VERIFY_DELETE_ALL_INLINE_KEYBOARD_MARKUP = generate_inline_keyboard('verify_delete_all')

# BOTS
BOT = telebot.TeleBot(token=TOKEN)


# DB CONNECTION
DB_CONN = create_conn()


# USER INSERT DICTS
USER_INSERTS = {}
CUSTOM_DATE = {}
WAITING_FOR_INSERT = {}


def set_user_spending_date(user_id, date):
    global CUSTOM_DATE
    CUSTOM_DATE[user_id] = date


def set_user_spending_dict(user_id, user_dict):
    global USER_INSERTS
    USER_INSERTS[user_id] = user_dict


def handle_current_date_input(message):

    #chat.id потому что  callback.message.from_user.id это id бота
    user_id = str(message.chat.id)
    user_date = get_current_date()

    set_user_spending_date(user_id, user_date)

    ask_for_input = load_command_reply_text('ask_for_input')
    ask_for_input_message = BOT.send_message(message.chat.id, ask_for_input)
    BOT.register_next_step_handler(ask_for_input_message, handle_insertion_input)


def handle_custom_date_input(message):

    #chat.id потому что  callback.message.from_user.id это id бота
    user_id = str(message.chat.id)
    user_date = message.text

    set_user_spending_date(user_id, user_date)

    ask_for_input = load_command_reply_text('ask_for_input')
    ask_for_input_message = BOT.send_message(message.chat.id, ask_for_input)
    BOT.register_next_step_handler(ask_for_input_message, handle_insertion_input)


def handle_insertion_input(message):
    try:
        user_id = str(message.from_user.id)
        user_date = CUSTOM_DATE[user_id]
        insertion_dict = parse_message_to_insert_dict(message.text, user_id, user_date)

        set_user_spending_dict(user_id, insertion_dict)

        validating_message = generate_validating_message(insertion_dict)
        BOT.send_message(message.chat.id, validating_message, reply_markup=VERIFY_INSERTION_INLINE_KEYBOARD_MARKUP)

    except Exception as e:
        print('handle_insertion_input', e)
        BOT.send_message(message.chat.id, 'Ошибка, не смог получить затрату')


def handle_rename_category_message(message):
    try:
        cat_before, cat_after = message.text.split()
        user_id = str(message.from_user.id)
        renaming_result = rename_category(user_id, cat_before, cat_after, DB_CONN)
        BOT.send_message(message.chat.id, renaming_result)

    except Exception as e:
        print('handle_rename_category ->', e)
        BOT.send_message(message.chat.id, 'Не смог получить категории')


@BOT.message_handler(commands=['start', 'help'])
def handle_start(message):
    reply_text = load_command_reply_text('help')
    commands_description = load_commands_description()

    reply_message = reply_text + '\n' + generate_validating_message(commands_description)

    BOT.send_message(message.chat.id, reply_message)


@BOT.message_handler(commands=['add_spending'])
def handle_add_spending(message):
    reply_text = load_command_reply_text('add_spending')
    BOT.send_message(message.chat.id, reply_text, reply_markup=CUSTOM_DATE_INLINE_KEYBOARD_MARKUP)


@BOT.message_handler(commands=['rename_category'])
def handle_rename_category(message):
    rename_category_reply = load_command_reply_text('rename_category')
    sent = BOT.send_message(message.chat.id, rename_category_reply)
    BOT.register_next_step_handler(sent, handle_rename_category_message)


@BOT.message_handler(commands=['show_categories'])
def handle_show_categories(message):
    reply_text = load_command_reply_text('show_categories') + '\n'

    categories_message = get_categories_message(str(message.from_user.id), DB_CONN)

    final_message = reply_text + categories_message

    BOT.send_message(message.chat.id, final_message)


@BOT.message_handler(commands=['delete_all'])
def handle_delete_all(message):
    reply_text = load_command_reply_text('delete_all')
    BOT.send_message(message.chat.id, reply_text, reply_markup=VERIFY_DELETE_ALL_INLINE_KEYBOARD_MARKUP)


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
            ask_for_date_input = load_command_reply_text('ask_for_date_input')
            sent = BOT.send_message(callback_chat_id, ask_for_date_input)
            BOT.register_next_step_handler(sent, handle_custom_date_input)

    elif 'verify_insertion' in call.data:
        
        if call.data == 'verify_insertion_true':
            saving_result = save_user_insertion(str(callback_user_id), USER_INSERTS, DB_CONN)
            BOT.send_message(callback_chat_id, saving_result)
        else:
            clear_user_insert_result = delete_user_insertion(str(callback_chat_id), USER_INSERTS)
            BOT.send_message(callback_chat_id, clear_user_insert_result)

    elif 'delete_all' in call.data:

        if call.data == 'delete_all_true':
            delete_all_result = delete_all_user_inserts(callback_chat_id, DB_CONN)
            BOT.send_message(callback_chat_id, delete_all_result)

        elif call.data == 'delete_all_false':
            BOT.send_message(callback_chat_id, 'Отменил удаление записей')




while True:
    BOT.polling(none_stop=True)