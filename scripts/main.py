import telebot
import json 
from config import BOT_CONFIG
from DbFuncs import *
from BotFuncs import *
from LoadData import *


TOKEN = BOT_CONFIG['API_TOKEN']


PLOTS_INLINE_KEYBOARD_MARKUP = generate_inline_keyboard('plots_keyboard')
DATE_FILTER_KEYBOARD_MARKUP = generate_inline_keyboard('date_filter_keyboard')
CUSTOM_DATE_INLINE_KEYBOARD_MARKUP = generate_inline_keyboard('add_spending_set_custom_date')
VERIFY_INSERTION_INLINE_KEYBOARD_MARKUP = generate_inline_keyboard('verify_insertion_keyboard')


BOT = telebot.TeleBot(token=TOKEN)


USER_INSERTS = {}
CUSTOM_DATE = {}
WAITING_FOR_INSERT = {}


def handle_insertion_input(message):
    user_id = message.from_user.id
    
    if not user_has_date(user_id=user_id, CUSTOM_DATE=CUSTOM_DATE):
        BOT.send_message(message.chat.id, 'Ошибка, нет даты затраты')
        return 
    
    insertion_dict = parse_message_to_insert_dict(message.text, user_id, load_user_spending_date(user_id, CUSTOM_DATE=CUSTOM_DATE))

    validation_message = generate_validating_message(insertion_dict)

    BOT.send_message(message.chat.id, validation_message,
                     reply_markup=VERIFY_INSERTION_INLINE_KEYBOARD_MARKUP)


def handle_custom_date_insertion_input(message):
    set_user_spending_date(message.from_user.id, CUSTOM_DATE, message.text)
    sent = BOT.send_message(message.chat.id, 'Введите затрату СТРОГО в формате категория название цена валюта (еда гамбургер 50 руб)')
    BOT.register_next_step_handler(sent, handle_insertion_input)


@BOT.message_handler(commands=['add_spending'])
def handle_add_spending(message):
    reply_text = load_command_reply_text('add_spending')

    BOT.send_message(message.chat.id, reply_text, reply_markup=CUSTOM_DATE_INLINE_KEYBOARD_MARKUP)


@BOT.message_handler(commands=['rename_category'])
def handle_rename_category(message):
    pass


@BOT.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    
    if 'spending_date' in call.data:

        if call.data == 'spending_date_today':
            set_user_spending_date(call.from_user.id, CUSTOM_DATE, get_current_date())
            ask_for_spending = BOT.send_message(call.message.chat.id, 'Введите затрату СТРОГО в формате категория название цена валюта (еда гамбургер 50 руб)')
            BOT.register_next_step_handler(ask_for_spending, handle_insertion_input)

        elif call.data == 'spending_date_custom':
            sent = BOT.send_message(call.message.chat.id, 'Введите дату строго в формате год-месяц-день(2022-03-01)')
            BOT.register_next_step_handler(sent, handle_custom_date_insertion_input)

    elif 'verify_insertion' in call.data:
        
        if call.data == 'verify_insertion_true':
            save_user_insertion(call.message.from_user.id, USER_INSERTS)
            BOT.send_message(call.message.chat.id, 'Успешно сохранил затрату в базу данных!')
        else:
            clear_user_insert(call.message.from_user.id, USER_INSERTS)
            BOT.send_message(call.message.chat.id, 'Отменил запись! Напишите /add_spending заново, чтобы записать новую затрату')


while True:
    BOT.polling(none_stop=True)