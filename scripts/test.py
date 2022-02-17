from db_funcs import *
from load_text import *
from plots import *
import datetime


initialize_db()

conn = create_conn()

insert_queries = [
    "INSERT INTO spendings VALUES('wjojf', '2022-02-01', 'food', 'cheesburger', 75.0, 'RUB')",
    "INSERT INTO spendings VALUES('wjojf', '2022-02-01', 'education', 'datacamp', 15.0, 'USD')",
    "INSERT INTO spendings VALUES('wjojf', '2022-02-01', 'games', 'nba2k22', 759.0, 'RUB')",
    "INSERT INTO spendings VALUES('wjojf', '2022-02-02', 'transport', 'autobus', 51.0, 'RUB')",
    "INSERT INTO spendings VALUES('wjojf', '2022-02-03', 'food', 'coffee', 180.0, 'RUB')",
    "INSERT INTO spendings VALUES('wjojf', '2022-02-04', 'food', 'coffee', 180.0, 'RUB')",
    "INSERT INTO spendings VALUES('wjojf', '2022-02-05', 'food', 'coffee', 180.0, 'RUB')",
    "INSERT INTO spendings VALUES('wjojf', '2022-02-06', 'food', 'coffee', 180.0, 'RUB')",
    "INSERT INTO spendings VALUES('wjojf', '2022-02-07', 'food', 'coffee', 180.0, 'RUB')",
    "INSERT INTO spendings VALUES ('wjojf', '2022-02-08', 'food', 'coffee', 180.0, 'RUB')"     
]

for insert_query in insert_queries:
    exec_insert_query(conn, insert_query)




spendings_groupby_date = get_spendings_groupby_date(conn, 'wjojf')
spendings_by_date_df = generate_df_from_db_rows(spendings_groupby_date, ('user_id', 'date', 'currency', 'money_spent'))
print(spendings_groupby_date)
res = spendings_barplot_by_date(spendings_by_date_df)
print(res)


delete_all_query = generate_delete_all_query('spendings')
exec_delete_query(conn, delete_all_query)