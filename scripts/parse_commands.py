from config import BOT_CONFIG

def command_is_valid(command: str, commands_json):
	return command in commands_json

def command_has_reply_text(command: str, commands_json):
    return 'reply_text' in commands_json[command]

def get_reply_text_by_command(command: str, commands_json):
	if command_is_valid(command, commands_json):
		if command_has_reply_text(command, commands_json):
			return commands_json[command]['reply_text']
		return ''
	return 'Нет такой команды'
