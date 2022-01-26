from load_text import load_json, CREDS_FILEPATH

BOT_CONFIG = {
	"API_TOKEN": load_json(CREDS_FILEPATH)['API_TOKEN'],
	"DB_DIR": "../db/",
	"STATIC_DIR": "../static/"
}
