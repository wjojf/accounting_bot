import LoadData as ld
import os
from config import BOT_CONFIG

STATIC_JSON_DIR = BOT_CONFIG['STATIC_JSON_DIR']
JSON_NEEDED_FILES = BOT_CONFIG['JSON_NEEDED_FILES']


def check_json_files():

    curr_json_dir = os.listdir(STATIC_JSON_DIR)

    if curr_json_dir == JSON_NEEDED_FILES:
        print('Все файлы найдены!')
    else:
        for filename in curr_json_dir:
            if filename not in JSON_NEEDED_FILES:
                print(f'Найден лишний файл: {filename}')
        not_found_files = [file for file in JSON_NEEDED_FILES if file not in curr_json_dir]
        if len(not_found_files) > 0:
            for not_found_file in not_found_files:
                print(f'Не найден: {not_found_file}')


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
