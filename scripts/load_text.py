import csv
import json 
from random import choice
from classify_intent import *
from config import BOT_CONFIG

'''FILEPATH'''

#BASE DIRS
STATIC_JSON_DIR = BOT_CONFIG['STATIC_JSON_DIR']
STATIC_TXT_DIR = BOT_CONFIG['STATIC_TXT_DIR']
STATIC_CSV_DIR = BOT_CONFIG['STATIC_CSV_DIR']

# JSON FILEPATH
COMMAND_REPLIES_JSON_FILEPATH = BOT_CONFIG['COMMAND_REPLIES_JSON_FILEPATH']
STICKERS_JSON_FILEPATH = BOT_CONFIG['STICKERS_JSON_FILEPATH']
TEXT_REPLIES_JSON_FILEPATH = BOT_CONFIG['TEXT_REPLIES_JSON_FILEPATH']
ADMINS_JSON_FILEPATH = BOT_CONFIG['ADMINS_JSON_FILEPATH']

# CSV FILEPATH
UNRECOGNIZED_COMMANDS_CSV_FILEPATH = BOT_CONFIG['UNRECOGNIZED_COMMANDS_CSV_FILEPATH']


# BASE FUNCS
def load_json(filepath: str):
	try:
		return json.load(open(filepath, encoding='utf-8'))
	except Exception as e:
		print(f'[LOAD_JSON] -> {e}')
		return

def clear_file(filepath):
	with open(filepath, 'w', encoding='utf-8') as unrecognized_commands_csv:
		pass

def load_csv(filepath: str):
	try:
		with open(filepath, 'r', encoding='utf-8') as csv_file:
			csv_reader = csv.reader(csv_file)
			return [row for row in csv_reader]

	except Exception as e:
		print(f'[load_csv] -> {e}')
		return -1



'''STATIC TEXT SECTION'''

# UNRECOGNIZED COMMANDS FUNCS
def add_unrecognized_command(message: str):
	with open(UNRECOGNIZED_COMMANDS_CSV_FILEPATH, 'a', encoding='utf-8', newline='') as unrecognized_commands_csv:
		csv_writer = csv.writer(unrecognized_commands_csv)
		try:
			csv_writer.writerow([message])
		except:
			print('[add_unrecognized_command] -> Could not')

# INTENT CLASSIFICATION
def get_intent_by_examples(message: str):
	text_replies_json = load_json(TEXT_REPLIES_JSON_FILEPATH)

	message = message.lower()

	if text_replies_json:
		for intent in text_replies_json:
			if message in text_replies_json[intent]['examples']:
				return intent
		return -1
	return -1


def get_intent_by_message(message: str):

	message = message.lower()

	intent_by_examples = get_intent_by_examples(message)
	predicted_intent = classify_intent_by_message()

	if intent_by_examples != -1:
		return intent_by_examples

	return predicted_intent


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


# stickers

def load_sticker_by_key(sticker_key: str):
	stickers_json = load_json(STICKERS_JSON_FILEPATH)

	try:
		return stickers_json[sticker_key]

	except KeyError:
		return -1

# commands 

def command_is_valid(command: str):
	commands_json = load_json(COMMAND_REPLIES_JSON_FILEPATH)

	if commands_json:
		return command in commands_json
	return False

def command_has_reply_text(command: str):
	commands_json = load_json(COMMAND_REPLIES_JSON_FILEPATH)

	if commands_json:
		return 'reply_text' in commands_json[command]
	return False


