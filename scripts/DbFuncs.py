from itertools import groupby
import sqlite3
import datetime
from config import BOT_CONFIG

# TODO: write select funcs for plot dfs(look plots.py for columns you need)


DB_FILEPATH = BOT_CONFIG['DB_FILEPATH']

# CREATE QUERIES

CREATE_SPENDINGS_TABLE_QUERY = f'''CREATE TABLE IF NOT EXISTS spendings(
                                                        user_id TEXT,
                                                        date TEXT,
                                                        category TEXT,
                                                        title TEXT,
                                                        price FLOAT,
                                                        currency TEXT
                                                )'''
CREATE_USER_CONFIG_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS user_config(user_id TEXT, user_status TEXT)'''
CREATE_ADMINS_CONFIG_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS admins(user_id TEXT, user_alias TEXT, admin_lvl TEXT)'''                                               


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


def create_conn():

    db_file = DB_FILEPATH
    conn = None

    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn

    except Exception as e:
        print(e)
        return None
        

def create_table(db_connection, create_query):
    connection_cursor = db_connection.cursor()

    try:
        connection_cursor.execute(create_query)
        db_connection.commit()
    except Exception as e:
        print('create_table error')
        print(e)


def exec_insert_query(table_connection, insertion_query):

    connection_cursor = table_connection.cursor()

    try:
        connection_cursor.execute(insertion_query)
        table_connection.commit()

    except Exception as e:
        print('exec_insert_query error')
        print(e)


def exec_select_query(table_connection, select_query):

    connection_cursor = table_connection.cursor()

    try:
        connection_cursor.execute(select_query)
        table_connection.commit()
        return connection_cursor.fetchall()
    except Exception as e:
        print('exec_select_query error')
        print(e)
        return None


def generate_select_all_query(table_name):
    return f'SELECT * FROM {table_name}'


def generate_select_query(table_name, columns, where=None, groupby=None, distinct=False):
    # handle columns
    if len(columns) == 1:
        columns_string = f'{columns[0]}'
    else:
        columns_string = ','.join(columns)

    query = f'SELECT {columns_string} FROM {table_name}'
    
    if distinct:
        query = query.replace('SELECT ', 'SELECT DISTINCT ')
    
    if where:
        where_joined = join_dict_values(where, ' AND ')
        query += f' WHERE {where_joined}'
    
    if groupby:

        if len(groupby) > 1:
            groupby_joined = ','.join(groupby)
        else:
            groupby_joined = groupby[0]
        query += f' GROUP BY {groupby_joined}'
    
    return query
        
    
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
        table_connection.commit()
    except Exception as e:
        print('exec_update_query ->', e)


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
        table_connection.commit()
    except Error as e:
        print(f'exec_delete_query -> {e}')


'''USER_CONFIG SECTION'''


def initialize_db():
    global DB_FILEPATH, CREATE_SPENDINGS_TABLE_QUERY, CREATE_USER_CONFIG_TABLE_QUERY

    conn = create_conn()
    # create tables
    print('creating tables')
    create_table(conn, CREATE_SPENDINGS_TABLE_QUERY)
    create_table(conn, CREATE_USER_CONFIG_TABLE_QUERY)
    create_table(conn, CREATE_ADMINS_CONFIG_TABLE_QUERY)
    print('tables created')
    # insert admins
    conn.close()


def insert_user_spending(spending_dict, conn):

    insert_query = generate_insert_query('spendings', spending_dict)
    print(insert_query)
    try:
        exec_select_query(conn, insert_query)
        print('Succesfully inserted user spending')

    except Exception as e:
        print(f'[insert_user_spending] -> {e}')


# plots section
def get_categoies_total_spendings(table_connection, user_id, table_name='spendings'):
    
    select_categories_spendings_query = generate_select_query(
                                    table_name,
                                    ('user_id', 'category', 'currency', "SUM(price)"),
                                    where={'user_id': user_id},
                                    groupby=('category', 'currency')
                                )

    categories_total_spenings = exec_select_query(table_connection, select_categories_spendings_query)

    return categories_total_spenings


def get_spendings_groupby_date(table_connection, user_id, table_name='spendings'):
    
    select_spendings_by_date_query = generate_select_query(
        table_name, ('user_id', 'date', 'currency', 'SUM(price)'),
        where={'user_id': user_id},
        groupby=('date', 'currency')
    )
    print(select_spendings_by_date_query)
    spendings_by_date = exec_select_query(table_connection, select_spendings_by_date_query)
    
    return spendings_by_date


def get_category_spendings(table_connection, user_id, category, table_name='spendings'):

    select_category_spendings_query = generate_select_query(
                            table_name,
                            ('user_id','category', 'date', 'currency', 'SUM(price)'),
                            where={
                                'user_id': user_id,
                                'category': category
                            },
                            groupby=['date', 'currency']
                        )
    print(select_category_spendings_query)
    category_spendings = exec_select_query(table_connection, select_category_spendings_query)

    return category_spendings