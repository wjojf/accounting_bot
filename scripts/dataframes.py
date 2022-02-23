import pandas as pd
from datetime import datetime


def load_df_from_db_rows(db_rows, columns):
    try:
        return pd.DataFrame(db_rows, columns=columns)
    except Exception as e:
        print(e)
        return


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
    curr_date = str(datetime.today().strftime('%Y-%m-%d'))

    curr_month_int = int(datetime.today().strftime('%m'))

    minus_3_months = int_year_to_str(minus_n_months(curr_month_int, n_months))

    date_min_list = curr_date.split('-')
    date_min_list[1] = minus_3_months

    return '-'.join(date_min_list)


def filter_today(df):
    today = datetime.today().strftime('%Y-%m-%d')
    return df[df['date'] == today]


def filter_this_year(df):
    current_year = datetime.today().strftime('%Y')
    return df[df['date'].year == current_year]


def filter_this_month(df):
    year_month = datetime.today().strftime('%Y-%m')
    return df[df['date'].strftime('%Y-%m') == year_month]


def filter_this_week(df):
    this_week = datetime.today().isocalendar()[1]
    return df[df['date'].isocalendar()[1] == this_week]


def filter_three_months(df):
    date_min = get_curr_date_minus_n_months(3)

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



