import telebot
import json 

# FUNCS

def get_API_token():
	with open('credentials.json') as json_file:
		return json.load(json_file)['API_TOKEN']

def get_reply_text_by_command(command: str):
	reply_texts_json = json.load(open('commands_text.json', encoding='utf-8'))
	try:
		return reply_texts_json[command.lower().strip()]
	except Exception:
		return 'Не понял полученную команду 😨'



# CONSTANTS

BOT_TOKEN = get_API_token()
bot = telebot.TeleBot(BOT_TOKEN)


# BOT LOOP

@bot.message_handler(commands=['start', 'commands'])
def start_message(message):
	command_text = message.text.replace('/', '')
	print(command_text)
	reply_message_text = get_reply_text_by_command(command_text)
	bot.send_message(message.chat.id, reply_message_text)


@bot.message_handler(commands=['add'])
def add_record(message):
	pass




while True:
	bot.polling(none_stop=True)
