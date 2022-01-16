import json 
from random import choice

#BASE DIRS
STATIC_DIR = '../static/'
STATIC_JSON_DIR = STATIC_DIR + 'json/'
STATIC_TXT_DIR = STATIC_DIR + 'txt/'

# JSON FILEPATH
COMMAND_REPLIES_JSON_FILEPATH = STATIC_JSON_DIR + 'commands_replies.json'
STICKERS_JSON_FILEPATH = STATIC_JSON_DIR + 'stickers.json'
TEXT_REPLIES_JSON_FILEPATH = STATIC_JSON_DIR + 'text_replies.json'

def load_json(filepath: str):
	try:
		return json.load(open(filepath, encoding='utf-8'))
	except Exception as e:
		print(f'[LOAD_JSON] -> {e}')
		return 


def get_text_reply_by_intent(intent: str) -> str:
	text_replies_json = load_json(TEXT_REPLIES_JSON_FILEPATH)

	if text_replies_json:
		print('ok')