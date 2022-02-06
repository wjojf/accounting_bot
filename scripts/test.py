from db_funcs import *
from load_text import *
from ml_funcs import *
import datetime

'''SPENDINGS TABLE TEST'''
# conn = create_conn(DB_FILEPATH)
# create_table(conn, CREATE_SPENDINGS_TABLE_QUERY)
#
# insert_dicts = [
#     {
#         'user_id': "id_1",
#         'date': str(datetime.datetime.now()),
#         'category': 'taxi',
#         'title': 'такси',
#         'price': 750,
#         'currency': 'RUB',
#         'ammount': 1
#     },
#
#     {
#         'user_id': "wjojf",
#         'date': str(datetime.datetime.now()),
#         'category': 'food',
#         'title': 'гамбургер',
#         'price': 50,
#         'currency': 'RUB',
#         'ammount': 1
#     },
#
#     {
#         'user_id': 'wjojf',
#         'date': str(datetime.datetime.now()),
#         'category': 'games',
#         'title': 'minecraft',
#         'price': 299,
#         'currency': 'RUB',
#         'ammount': 1
#     },
#
# ]
#
# for insert_dict in insert_dicts:
#     query = generate_insert_query('spendings', insert_dict)
#     exec_insert_query(conn, query)
#
# print('AFTER FIRST INSERT')
#
# select_all_query = generate_select_all_query('spendings')
# rows = exec_select_query(conn, select_all_query)
# for row in rows:
#     print(*row)
# print()
# print('UPDATING SOME VALUES')
# print()
# update_query = generate_update_query('spendings', {'price': 75, 'ammount': 2},{'user_id': "wjojf", 'category': 'food'})
# exec_update_query(conn, update_query)
#
# rows = exec_select_query(conn, select_all_query)
# for row in rows:
#     print(*row)
# print()
# print('GROUP BY MULTIPLE COLUMNS')
# print(get_unique_categories_by_user_id(conn,'spendings','wjojf'))
#
# print('')

'''USER CONFIG TABLE TEST'''

conn = create_conn(DB_FILEPATH)
create_table(conn, CREATE_USER_CONFIG_TABLE_QUERY)

test_inserts = [
    {
        'user_id': 'wjojf',
        'user_status': 'admin'
    },
    {
        'user_id': 'not_wjojf',
        'user_status': 'user'
    }

]

for insert in test_inserts:
    query = generate_insert_query('user_config', insert)
    exec_insert_query(conn, query)

select_all_query = generate_select_all_query('user_config')
res = exec_select_query(conn, select_all_query)
for record in res:
    print(record)

