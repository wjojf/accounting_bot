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

# BOTS
BOT = telebot.TeleBot(token=TOKEN)


# DB CONNECTION
DB_CONN = create_conn()


# USER INSERT DICTS
USER_INSERTS = {}
CUSTOM_DATE = {}
WAITING_FOR_INSERT = {}


def handle_custom_date_input(message):
    set_user_spending_date(message.from_user.id, message.text)


def set_user_spending_date(user_id, date):
    global CUSTOM_DATE
    CUSTOM_DATE[user_id] = date


def set_user_spending_dict(user_id, user_dict):
    global USER_INSERTS
    USER_INSERTS[user_id] = user_dict


def handle_insertion_input(message):
    try:
        user_id = message.from_user.id
        user_date = CUSTOM_DATE[user_id]
        insertion_dict = parse_message_to_insert_dict(user_id, user_date, message.text)
        set_user_spending_dict(message.from_user.id, insertion_dict)
        validating_message = generate_validating_message(insertion_dict)
        BOT.send_message(message.chat.id, validating_message, reply_markup=VERIFY_INSERTION_INLINE_KEYBOARD_MARKUP)

    except Exception as e:
        print('handle_insertion_input', e)
        BOT.send_message(message.chat.id, 'Ошибка, не смог получить')


@BOT.message_handler(commands=['add_spending'])
def handle_add_spending(message):
    reply_text = load_command_reply_text('add_spending')
    BOT.send_message(message.chat.id, reply_text, reply_markup=CUSTOM_DATE_INLINE_KEYBOARD_MARKUP)


@BOT.message_handler(commands=['rename_category'])
def handle_rename_category(message):
    sent = BOT.send_message(message.chat.id, 'Введите категорию которую хотите переименовать и новое название через пробел(mcdonalds food)')
    BOT.message_handler(sent, rename_category_preparation)


@BOT.message_handler(commands=['show_categories'])
def hande_show_categories(message):
    reply_text = load_command_reply_text('show_categories') + '\n'

    categories_message = get_categories_message(message.from_user.id, DB_CONN)

    final_message = reply_text + categories_message

    BOT.send_message(message.chat.id, final_message)


@BOT.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    
    if 'spending_date' in call.data:
        ask_for_input_reply = load_command_reply_text('ask_for_input')

        if call.data == 'spending_date_today':

            set_user_spending_date(call.from_user.id, get_current_date())

            ask_for_input = BOT.send_message(call.message.chat.id, ask_for_input_reply)
            BOT.register_next_step_handler(ask_for_input, handle_insertion_input)

        elif call.data == 'spending_date_custom':

            reply_message = load_command_reply_text['custom_date_input']
            sent_date = BOT.send_message(call.message.chat.id, reply_message)
            BOT.register_next_step_handler(sent_date, handle_custom_date_input)
            ask_for_input = BOT.send_message(call.chat.id, ask_for_input_reply)
            BOT.register_next_step_handler(ask_for_input, handle_insertion_input)

    elif 'verify_insertion' in call.data:
        
        if call.data == 'verify_insertion_true':
            result = save_user_insertion(call.from_user.id, USER_INSERTS)
            BOT.send_message(call.chat.id, result)

        else:
            result = clear_user_insertion(call.from_user.id, USER_INSERTS)
            BOT.send_message(call.chat.id, result)


while True:
    BOT.polling(none_stop=True)