from DbFuncs import *

conn = create_conn()

insert_query = '''INSERT INTO spendings VALUES ('wjojf', '2022-03-07', 'food', 'hamburger', 50, 'RUB')'''
exec_insert_query(conn, insert_query)




select_all_query = generate_select_all_query('spendings')

print(select_all_query)

print(exec_select_query(conn, select_all_query))

delete_all_query = generate_delete_all_query('spendings')

print(delete_all_query)

exec_delete_query(conn, delete_all_query)

print(exec_select_query(conn, select_all_query))


conn.close()