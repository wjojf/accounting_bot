import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


def load_df_from_db_rows(db_rows, columns=['user_id', 'date', 'category', 'title', 'price', 'currency']):

    '''
    :param db_rows: list of tuples (db rows values)
    :param columns: column names for dataframe
    :return: pandas DataFrame/ None
    '''

    try:
        return pd.DataFrame(db_rows, columns=columns)
    except Exception as e:
        print(e)
        return


def parse_date_for_df(df):
    df['date'] = df['date'].apply(lambda x: datetime.fromisoformat(x))
    return df


def date_to_str_for_df(df):
    df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    return df


def minus_n_months(curr_month: int, n: int):
    if curr_month > n:
        return curr_month - n
    if curr_month == n:
        return 12
    return 12 - (n - curr_month)


def int_year_to_str(int_year):
    if int_year >= 10:
        return str(int_year)
    return '0' + str(int_year)


def get_curr_date_minus_n_months(n_months):
    return (datetime.now() - relativedelta(months=n_months)).strftime('%Y-%m-%d')


def filter_today(df):
    today = datetime.today().strftime('%Y-%m-%d')

    return df[df['date'] == today]


def filter_this_year(df):
    current_year = datetime.today().strftime('%Y')
    condition = df['date'].apply(lambda x: x.year == current_year)
    return df[condition]


def filter_this_month(df):
    year_month = datetime.today().strftime('%Y-%m')

    condition = df['date'].apply(lambda x: x.strftime('%Y-%m') == year_month)

    return df[condition]


def filter_this_week(df):
    this_week = datetime.today().isocalendar()[1]
    condition = df['date'].apply(lambda x: x.isocalendar()[1] == this_week)
    return df[condition]


def filter_three_months(df):
    date_min = get_curr_date_minus_n_months(3)
    print(date_min)
    return filter_by_datemin_datemax(df, date_min=date_min)


def filter_six_months(df):
    date_min = get_curr_date_minus_n_months(6)

    return filter_by_datemin_datemax(df, date_min=date_min)


def filter_by_datemin_datemax(df, date_min=None, date_max=None):

    if date_min:
        if date_max:
            return df[(df['date'] >= date_min) & (df['date'] <= date_max)]
        return df[df['date'] >= date_min]

    if date_max:
        return df[df['date'] <= date_max]

    return df


def filter_df_by_date(df, date_filter_mode=None, date_min=None, date_max=None):
    date_filter_mode_funcs = {
        'today': filter_today,
        'last_week': filter_this_week,
        'this_month': filter_this_month,
        'three_months': filter_three_months,
        'six_months': filter_six_months,
        'this_year': filter_this_year
    }

    if date_filter_mode in date_filter_mode_funcs:
        return date_filter_mode_funcs[date_filter_mode](df)

    if date_min or date_max:
        return filter_by_datemin_datemax(df, date_min, date_max)


