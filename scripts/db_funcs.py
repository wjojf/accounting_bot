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
CREATE_USER_CONFIG_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS user_config(user_id TEXT, user_status TEXT)'''
                                                          

def join_dict_values(_dict, out_separator=','):
    joined = []

    if len(_dict.keys()) == 1:
        k = list(_dict.keys())[0]
        v = list(_dict.values())[0]

        if isinstance(v, str):
            return '='.join([k, f"'{v}'"])
        return '='.join([str(x) for x in [k,v]])

    for k, v in _dict.items():
        if isinstance(v, str):
            joined.append('='.join([k, f"'{v}'"]))
        else:
            joined.append('='.join([str(x) for x in [k,v]]))

    return out_separator.join(joined)

def get_result_of_query(cursor):
    return cursor.fetchall()


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
        connection_cursor.execute(select_query)
        return connection_cursor.fetchall()
    except Exception as e:
        print('exec_select_query error')
        print(e)
        return None

def generate_select_all_query(table_name):
    return f'SELECT * FROM {table_name}'

def generate_select_query(table_name, columns, where=None, distinct=False):
    # handle columns
    if len(columns) == 1:
        columns_string = f'{columns[0]}'
    else:
        columns_string = ','.join(columns)



    if where == None:
        if distinct:
            return f'''SELECT DISTINCT {columns_string} FROM {table_name}'''
        return  f'''SELECT {columns_string} FROM {table_name}'''

    where_joined = join_dict_values(where, ' AND ')
    if distinct:
        return f'''SELECT DISTINCT {columns_string} FROM {table_name} WHERE {where_joined}'''
    return f'''SELECT {columns_string} FROM {table_name} WHERE {where_joined}'''

def generate_update_query(table_name, update_values, where_values):


    update_joined = join_dict_values(update_values)
    where_joined = join_dict_values(where_values, ' AND ')

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


# TODO: fix selecting multiple columns bug

def get_unique_categories_by_user_id(table_connection,table_name, user_id):

    unique_categories_query = generate_select_query(table_name,
                                                    ['category'],
                                                    where={'user_id': user_id},
                                                    distinct=True)

    categories = exec_select_query(table_connection, unique_categories_query)
    categories = [cat[0] for cat in categories]

    unique_currenices_query = generate_select_query(
        table_name,
        ['currency'],
        where={'user_id': user_id},
        distinct=True
    )
    currencies = exec_select_query(table_connection, unique_currenices_query)
    currencies = [curr[0] for curr in currencies]

    output_dict = {}
    for category in categories:

        if category not in output_dict.keys():
            output_dict[category] = {}

        for currency in currencies:

            if currency not in output_dict[category].keys():
                output_dict[category][currency] = 0

            price_ammount_query = generate_select_query(
                table_name,
                ('price', 'ammount'),
                where={'user_id': user_id, 'category': category, 'currency': currency}
            )
            print(price_ammount_query)
            price_ammount = exec_select_query(table_connection, price_ammount_query)

            for record in price_ammount:
                p, a = record
                output_dict[category][currency] += p*a

    return output_dict


'''USER_CONFIG SECTION'''

def get_user_status(table_connection, user_id):
    select_query = generate_select_query('user_config', ['user_status'])

    return exec_select_query(table_connection, select_query)






