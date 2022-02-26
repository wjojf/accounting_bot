from plots import *
import pprint
from load_text import load_json
from config import BOT_CONFIG
printer = pprint.PrettyPrinter()

stickers = load_json(BOT_CONFIG['STICKERS_JSON_FILEPATH'])
printer.pprint(stickers)