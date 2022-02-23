from config import BOT_CONFIG
import re
import pprint
printer = pprint.PrettyPrinter()


def split_words(message: str):
    rgx = re.compile("([\w][\w']*\w)")
    return rgx.findall(message)

def parse_currency(currency_from_message: str):
    
    currency_map = {
        'RUB': ['руб', 'р', 'рубль'],
        "USD": ['usd', 'доллар'],
        "EUR": ['eur', 'eu', 'евро']
    }
        
    for currency in currency_map:
        for message_example in currency_map[currency]:
            if currency_from_message == message_example:
                return currency
    
    return None


def get_intent_by_message(message: str):

	message = message.lower()

	intent_by_examples = get_intent_by_examples(message)
	predicted_intent = classify_intent_by_message()

	if intent_by_examples != -1:
		return intent_by_examples

	return predicted_intent



def split_user_spending_message(user_message: str):
    #splits user message and returns a list of needed dtypes for db insert
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


    except:
        return
    




print(split_words('еда гамбурге 50 руб'))
