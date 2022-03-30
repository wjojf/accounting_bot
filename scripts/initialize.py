import LoadData as ld
import os
from config import BOT_CONFIG

STATIC_JSON_DIR = BOT_CONFIG['STATIC_JSON_DIR']


def check_json_files():
    pass


def initialize_repository():

    try:
        print('Удаляю устаревшие графики...')
        ld.clear_png_folder()
        print('Успещно очистил папку с графиками...')

        print('Проверяю наличие всех json файлов...')
        check_json_files()
        print('Успешно проверил наличие всех json файлов...')


        print('Готов к работе!')
    except Exception as e:
        print(e)
