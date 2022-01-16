import sqlite3
import datetime

DB_FILEPATH = './db/DATABASE.db'
TABLE_NAME = 'records'
CREATE_TABLE_QUERY = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                                        user_id text,
                                        date text,
                                        category text,
                                        price integer,
                                        comment text 
                                );"""


def create_conn(db_file):

    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


    return conn


def create_table(conn, create_table_sql_query):

    try:
        c = conn.cursor()
        c.execute(create_table_sql_query)
        print('Successfully created table!')
    except Exception as e:
        print(f'[ERROR] -> {e}')


def create_bot_db():
    global DB_FILEPATH, CREATE_TABLE_QUERY

    db_connection = create_conn(DB_FILEPATH)

    if db_connection is not None:
        create_table(db_connection, CREATE_TABLE_QUERY)
    else:
        print('[ERROR] -> No connection to database')


def insert_record(record_dict: dict):
    global DB_FILEPATH, TABLE_NAME

    to_insert_keys = list(record_dict.keys())
    to_insert_values = list(record_dict.values())

    print(to_insert_keys)
    print(to_insert_values)

    INSERT_QUERY = "INSERT INTO {0} ({1}, {2}, {3}, {4}, {5}) VALUES({6}, {7}, {8}, {9}, {10})".format(TABLE_NAME, *to_insert_keys, *to_insert_values)

    db_connection = create_conn(DB_FILEPATH)
    cursor = db_connection.cursor()


    try:
        cursor.execute(INSERT_QUERY)
    except Exception as e:
        print(f'[ERROR] -> {e}')


def load_data():
    global DB_FILEPATH, TABLE_NAME

    conn = create_conn(DB_FILEPATH)
    c = conn.cursor()
    c.execute(f'SELECT * FROM {TABLE_NAME}')

    rows = c.fetchall()
    conn.close()

    rows = [list(x) for x in rows]

    for row in rows:
        print(row)




def test():
    global DB_FILEPATH

    test_insert = {
        'user_id': 'my_id',
        'date': '2022-01-03',
        'category': 'food',
        'price': 400,
        'comment': None
    }

    insert_record(test_insert)

    load_data()



if __name__ == '__main__':
    create_bot_db()
    test()
