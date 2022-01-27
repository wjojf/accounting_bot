from db_funcs import *
from load_text import *
from ml_funcs import *
import datetime

conn = create_conn(DB_FILEPATH)
create_table(conn, CREATE_SPENDINGS_TABLE_QUERY)

insertion_dict = {
    'user_id': "last",
    'date': str(datetime.datetime.now()),
    'category': 'taxi',
    'title': 'такси',
    'price': 750,
    'currency': 'RUB',
    'ammount': 1
}
INSERTION_QUERY = generate_insert_query('spendings', insertion_dict)
print(INSERTION_QUERY)
exec_insert_query(conn, INSERTION_QUERY)

result = exec_select_query(conn, generate_select_all_query('spendings'))
print(result)

update_values = {'user_id': 'new_last', 'price': 850}
where_values = {'user_id': 'last'}



update_query = generate_update_query('spendings', update_values, where_values)
print(update_query)
exec_update_query(conn, update_query)

result = exec_select_query(conn, generate_select_all_query('spendings'))
print(result)


DELETE_ALL_QUERY = generate_delete_all_query('spendings')
exec_delete_query(conn, DELETE_ALL_QUERY)

result = exec_select_query(conn, generate_select_all_query('spendings'))
print(result)