import csv
import json 
from random import choice
from ml_funcs import *

#BASE DIRS
STATIC_DIR = '../static/'
STATIC_JSON_DIR = STATIC_DIR + 'json/'
STATIC_TXT_DIR = STATIC_DIR + 'txt/'
STATIC_CSV_DIR = STATIC_DIR + 'csv/'

# JSON FILEPATH
COMMAND_REPLIES_JSON_FILEPATH = STATIC_JSON_DIR + 'commands_replies.json'
STICKERS_JSON_FILEPATH = STATIC_JSON_DIR + 'stickers.json'
TEXT_REPLIES_JSON_FILEPATH = STATIC_JSON_DIR + 'text_replies.json'

# CSV FILEPATH
UNRECOGNIZED_COMMANDS_CSV_FILEPATH = STATIC_CSV_DIR + 'unrecognized_commands.csv'

def load_json(filepath: str):
	try:
		return json.load(open(filepath, encoding='utf-8'))
	except Exception as e:
		print(f'[LOAD_JSON] -> {e}')
		return 


def add_unrecognized_command(message: str):
	with open(UNRECOGNIZED_COMMANDS_CSV_FILEPATH, 'a', encoding='utf-8', newline='') as unrecognized_commands_csv:
		csv_writer = csv.writer(unrecognized_commands_csv)
		try:
			csv_writer.writerow([message])
		except:
			pass 	

def load_unrecognized_commands():
	with open(UNRECOGNIZED_COMMANDS_CSV_FILEPATH, 'r', encoding='utf-8') as unrecognized_commands_csv:
		csv_reader = csv.reader(unrecognized_commands_csv)

		for i, row in enumerate(csv_reader):
			print(f'{i+1}) {row}')

def clear_unrecognized_commands():
	with open(UNRECOGNIZED_COMMANDS_CSV_FILEPATH, 'w', encoding='utf-8') as unrecognized_commands_csv:
		pass

def get_intent_by_keywords(message: str):
	text_replies_json = load_json(TEXT_REPLIES_JSON_FILEPATH)

	message = message.lower()

	if text_replies_json:
		for intent in text_replies_json.keys():
			for keyword in text_replies_json[intent]['keywords']:
				if keyword in message:
					return intent 

		add_unrecognized_command(message)
		return -1

	return -1



def get_text_reply_by_intent(intent: str) -> str:
	text_replies_json = load_json(TEXT_REPLIES_JSON_FILEPATH)

	if text_replies_json:
		try:
			return text_replies_json[intent]
		except KeyError:
			print(f'[get_text_reply_by_intent] -> no such intent as {intent}')
			return -1

	print('[get_text_reply_by_intent] -> could not load json')
	return -1




def test_func():
	result = get_intent_by_keywords('привет! как твои дела?')
	print(result)
if __name__ == '__main__':
	test_func()


