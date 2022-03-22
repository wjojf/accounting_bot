import os
import csv
import json
from config import BOT_CONFIG
from datetime import datetime


STATIC_JSON_DIR = BOT_CONFIG['STATIC_JSON_DIR']
STATIC_TXT_DIR = BOT_CONFIG['STATIC_TXT_DIR']
STATIC_CSV_DIR = BOT_CONFIG['STATIC_CSV_DIR']
STATIC_PNG_DIR = BOT_CONFIG['STATIC_PNG_DIR']


COMMAND_REPLIES_JSON_FILEPATH = BOT_CONFIG['COMMAND_REPLIES_JSON_FILEPATH']
STICKERS_JSON_FILEPATH = BOT_CONFIG['STICKERS_JSON_FILEPATH']
TEXT_REPLIES_JSON_FILEPATH = BOT_CONFIG['TEXT_REPLIES_JSON_FILEPATH']
ADMINS_JSON_FILEPATH = BOT_CONFIG['ADMINS_JSON_FILEPATH']


UNRECOGNIZED_COMMANDS_CSV_FILEPATH = BOT_CONFIG['UNRECOGNIZED_COMMANDS_CSV_FILEPATH']


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


def load_command_reply_text(command):
	commands_json = load_json(COMMAND_REPLIES_JSON_FILEPATH)
	if command in commands_json:
		return commands_json[command]['reply_text']
	
	return f'Ты вызвал комманду {command}'


def load_commands_description():
	return load_json(COMMAND_REPLIES_JSON_FILEPATH)['help']['commands_description']


def add_unrecognized_command(message: str):
	with open(UNRECOGNIZED_COMMANDS_CSV_FILEPATH, 'a', encoding='utf-8', newline='') as unrecognized_commands_csv:
		csv_writer = csv.writer(unrecognized_commands_csv)
		try:
			csv_writer.writerow([message])
		except:
			print('[add_unrecognized_command] -> Could not')


def load_sticker_by_key(sticker_key: str):
	stickers_json = load_json(STICKERS_JSON_FILEPATH)

	try:
		return stickers_json[sticker_key]

	except KeyError:
		return -1


# img 

def img_exists(filepath: str):
	if filepath.endswith('.png'):
		return filepath in os.listdir(STATIC_PNG_DIR)
	return False


def images_by_user_id(user_id: str):
	return [filepath for filepath in os.listdir(STATIC_PNG_DIR) if user_id in filepath]


def images_by_user_id_and_plot_type(user_id: str, plot_type: str):
	return [
		filepath for filepath in os.listdir(STATIC_PNG_DIR) 
		if user_id in filepath and plot_type in filepath
	]


# dates


def get_current_date():
	return str(datetime.now().strftime('%Y-%m-%d'))

