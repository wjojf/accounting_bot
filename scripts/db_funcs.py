import sqlite3
import datetime

DB_FILEPATH = './db/DATABASE.db'

SPENDINGS_TABLE_NAME = 'spendings'
CREATE_SPENDINGS_TABLE_QUERY = f'''CREATE TABLE IF NOT EXISTS {SPENDINGS_TABLE_NAME}(
                                                        user_id TEXT,
                                                        date TEXT,
                                                        category TEXT,
                                                        price FLOAT,
                                                        currency TEXT,
                                                        ammount INT
                                                            )'''


def create_conn(db_file):

    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn

    except Exception as e:
        print(e)
        return None
        

def create_table(db_connection, create_query):
    connection_cursor = db_connection.cursor()

    try:
        connection_cursor.execute(create_query)
    except Exception as e:
        print(e)


def exec_insert_query(table_connection, insertion_query):

    connection_cursor = table_connection.cursor()

    try:
        connection_cursor.execute(insertion_query)

    except Exception as e:
        print(e)


def exec_select_query(table_connection, select_query):

    connection_cursor = table_connection.cursor()

    try:
        rows = connection_cursor.execute(select_query)
        return [row for row in rows]

    except Exception as e:
        print(e)
        return None


def generate_select_query(table_name, *columns):
    return f'''SELECT {columns} FROM {table_name}'''


def change_val(table_name, table_connection, update_values, where_values):
    connection_cursor = table_connection.cursor()

    values_joined = ['='.join([k, v]) for k, v in update_values.items()]
    where_joined = ['='.join([k, v]) for k, v in update_values.items()]

    connection_cursor.execute(f'''
        UPDATE {table_name}
        SET {','.join(values_joined)}
        WHERE {','.join(where_joined)}
    ''')





