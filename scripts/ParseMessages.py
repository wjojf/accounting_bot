import re
import LoadData as ld
from config import BOT_CONFIG
from random import choice


def split_words(message: str):
    rgx = re.compile("([\w][\w']*\w)")
    return rgx.findall(message)


def parse_currency(currency_from_message: str):
    
    currency_map = {
        'RUB': ['руб', 'р', 'рубль', 'rub', 'ru'],
        "USD": ['usd', 'доллар'],
        "EUR": ['eur', 'eu', 'евро']
    }
        
    for currency in currency_map:
        for message_example in currency_map[currency]:
            if currency_from_message == message_example:
                return currency
    
    return None


def split_user_spending_message(user_message: str):
    return split_words(user_message)


def parse_message_to_insert_dict(user_message: str, user_id, date):
    # gets list of splitted message with needed dtypes for insertion 
    # and creates and insertion_dict for db_func exec_insert_query to run
    message_splitted = split_words(user_message)

    try:
        category, title, price, currency = message_splitted

        return {
            'user_id': user_id,
            'date': date,
            'category':  category,
            'title': title,
            'price': price,
            'currency': parse_currency(currency) 
        }
    except Exception as e:
        print(e)
        return


def generate_validating_message(insertion_dict):

    dict_strings = [f'📍{k}: {v}' for k,v in insertion_dict.items()]

    return '\n' + '\n'.join(dict_strings)


def classifyIntent(message):
    message_lower = message.lower()

    text_replies_json = ld.load_json(BOT_CONFIG["TEXT_REPLIES_JSON_FILEPATH"])

    for intent in text_replies_json:
        for keyword in text_replies_json[intent]['keywords']:
            if message_lower in keyword:
                return intent
    return None


def loadIntentAnswer(intent):

    text_replies_json = ld.load_json(BOT_CONFIG["TEXT_REPLIES_JSON_FILEPATH"])

    try:
        return choice(text_replies_json[intent]['replies'])
    except Exception as e:
        print(e)
        return 'Не понял тебя:('


def loadUnknownIntentAnswer():
    return 'Не понимаю тебя. Спроси что-нибудь другое'