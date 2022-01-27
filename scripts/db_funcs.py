import sqlite3
import datetime

DB_FILEPATH = '../db/DATABASE.db'

SPENDINGS_TABLE_NAME = 'spendings'
CREATE_SPENDINGS_TABLE_QUERY = f'''CREATE TABLE IF NOT EXISTS {SPENDINGS_TABLE_NAME}(
                                                        user_id TEXT,
                                                        date TEXT,
                                                        category TEXT,
                                                        title TEXT,
                                                        price FLOAT,
                                                        currency TEXT,
                                                        ammount INT
                                                            )'''


def join_dict_values(_dict):
    joined = []
    for k, v in _dict.items():
        if isinstance(v, str):
            joined.append('='.join([k, f"'{v}'"]))
        else:
            joined.append('='.join([str(x) for x in [k,v]]))

    return ','.join(joined)


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
        print('create_table error')
        print(e)


def exec_insert_query(table_connection, insertion_query):

    connection_cursor = table_connection.cursor()

    try:
        connection_cursor.execute(insertion_query)

    except Exception as e:
        print('exec_insert_query error')
        print(e)


def exec_select_query(table_connection, select_query):

    connection_cursor = table_connection.cursor()

    try:
        rows = connection_cursor.execute(select_query)
        return [row for row in rows]

    except Exception as e:
        print('exec_select_query error')
        print(e)
        return None

def generate_select_all_query(table_name):
    return f'SELECT * FROM {table_name}'

def generate_select_query(table_name, *columns):
    return f'''SELECT {columns} FROM {table_name}'''


def generate_update_query(table_name, update_values, where_values):


    update_joined = join_dict_values(update_values)
    where_joined = join_dict_values(where_values)

    return f'''
        UPDATE {table_name}
        SET {update_joined}
        WHERE {where_joined}
    '''

def exec_update_query(table_connection, update_query):
    connection_cursor = table_connection.cursor()

    try:
        connection_cursor.execute(update_query)
    except Exception as e:
        print('')

def generate_insert_query(table_name, column_values_dict):
    return f'INSERT INTO {table_name} {tuple(column_values_dict.keys())} VALUES {tuple(column_values_dict.values())}'

def generate_delete_all_query(table_name):
    return f'DELETE FROM {table_name}'


def generate_delete_query(table_name, where):
    where_joined = ','.join(['='.join([k,v]) for k,v in where.items])
    return f'''DELETE FROM {table_name} WHERE {where_joined}'''


def exec_delete_query(table_connection, delete_query):
    connection_cursor = table_connection.cursor()

    try:
        connection_cursor.execute(delete_query)
    except Error as e:
        print(f'exec_delete_query -> {e}')


