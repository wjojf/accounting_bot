from plots import *
#import datetime


df_rows = [
            ('wjojf', '2022-02-01', 'food', 'cheesburger', 75.0, 'RUB'),
            ('wjojf', '2022-02-01', 'education', 'datacamp', 15.0, 'USD'),
            ('wjojf', '2022-02-01', 'games', 'nba2k22', 759.0, 'RUB'),
            ('wjojf', '2022-02-02', 'transport', 'autobus', 51.0, 'RUB'),
            ('wjojf', '2022-02-03', 'food', 'coffee', 180.0, 'RUB'),
            ('wjojf', '2022-02-04', 'food', 'coffee', 180.0, 'RUB'),
            ('wjojf', '2022-02-05', 'food', 'coffee', 180.0, 'RUB'),
            ('wjojf', '2022-02-06', 'food', 'coffee', 180.0, 'RUB'),
            ('wjojf', '2022-02-07', 'food', 'coffee', 180.0, 'RUB'),
            ('wjojf', '2022-02-08', 'food', 'coffee', 180.0, 'RUB'),
            ('wjojf', '2022-02-08', 'food', 'coffee', 100.0, 'USD')
        ]

df = pd.DataFrame(df_rows, columns=['user_id', 'date', 'category', 'title', 'price', 'currency'])

grouped_by_date_currency = df.groupby(['user_id', 'date', 'currency']).agg({'price': 'sum'}).reset_index().sort_values(by='date')

res = spendings_lineplot_by_date(grouped_by_date_currency)
print(res)

res = spendings_barplot_by_date(grouped_by_date_currency)
print(res)

grouped_by_category_currency = df.groupby(['user_id', 'category', 'currency']).agg({'price': 'sum'}).reset_index()

res = categories_barplot_by_currency(grouped_by_category_currency)
print(res)

res = categories_pieplot_by_currency(grouped_by_category_currency)
print(res)