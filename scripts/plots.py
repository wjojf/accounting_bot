import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 
import datetime as dt
from config import BOT_CONFIG


PNG_DIR = BOT_CONFIG['STATIC_PNG_DIR']

def generate_plot_filepath(user_id, plot_type, date_min=None, date_max=None):
    
    plot_filepath = f'{PNG_DIR}{user_id}_{plot_type}'
    
    
    if date_min:
        plot_filepath += f'{date_min}'
        if date_max:
            plot_filepath += f'{date_max}'
        else:
            curr_date = dt.datetime.now()
            date_max = f'{curr_date.year}-{curr_date.month}-{curr_date.day}'
            plot_filepath += date_max
    
    return plot_filepath


'''DataFrames'''


def generate_df_from_db_rows(db_rows, column_names):
    df = pd.DataFrame(db_rows, columns=column_names)
    return df


def filter_df_by_date(user_df, date_min=None, date_max=None):
    
    if date_min:
        if date_max:
            return user_df[(user_df['date'] >= date_min) & (user_df['date'] <= date_max)]
        return user_df[(user_df['date'] >= date_min)]
    return user_df


'''Lineplots'''


def spendings_lineplot_by_date(user_data, plot_type='spendings_lineplot_by_date', date_min=None, date_max=None):

    user_id = list(user_data['user_id'])[0]

    try:
        currency_grid = sns.FacetGrid(user_data, col='currency', height=3, aspect=1.33, margin_titles=True)
        currency_grid.map(sns.pointplot, 'date', 'price')
        #currency_grid.set_axis_labels(x_var='date', y_var='spent')

        plot_filepath = generate_plot_filepath(user_id, plot_type, date_min, date_max)
        plt.savefig(plot_filepath)
        print('Успешно сохранена картинка')
        return plot_filepath

    except Exception as e:
        print(e)
        return BOT_CONFIG['ERROR_IMAGE_FILEPATH']


'''barplots'''


def spendings_barplot_by_date(user_data, plot_type='spendings_barplot_by_date'):
    try:
        fig, ax = plt.subplots(figsize=(9, 9))
        sns.barplot(x='date', y='price', data=user_data, hue='currency', ax=ax)
        plt.xticks(rotation=90)
        plt.xlabel('Дата')
        plt.ylabel('Сумма Затрат')
        plt.title(f'Затраты {list(user_data["user_id"])[0]}')
        #plt.set_xticklabels([user_data['date'].min(), user_data['date'].max()])

        filepath = generate_plot_filepath(list(user_data['user_id'])[0], plot_type)
        plt.savefig(filepath)
        print('Успешно сохранена картинка')
        return filepath

    except Exception as e:
        print(e, BOT_CONFIG['ERROR_IMAGE_FILEPATH'])


def categories_barplot_by_currency(user_data, plot_type='categoris_barplot_by_currency'):
    try:
        fig, ax = plt.subplots(figsize=(10,10))
        sns.barplot(x='category', y='price', data=user_data, hue='currency', ax=ax)
        plt.xticks(rotation=90)
        plt.xlabel('Дата')
        plt.ylabel('Сумма Затрат')
        plt.title(f'Затраты {list(user_data["user_id"])[0]}')
        #plt.set_xticklabels([user_data['date'].min(), user_data['date'].max()])

        filepath = generate_plot_filepath(list(user_data['user_id'])[0], plot_type)
        plt.savefig(filepath)
        print('Успешно сохранена картинка')
        return filepath

    except Exception as e:
        print(e)
        return BOT_CONFIG['ERROR_IMAGE_FILEPATH']

'''pieplots'''

def categories_pieplot_by_currency(user_data, plot_type='categories_pieplot_by_currency'):

    def plot_pie(x, labels, **kwargs):
        plt.pie(x=x, labels=labels)

    user_id = list(user_data['user_id'])[0]

    try:
        grid = sns.FacetGrid(user_data, col='currency',height=3, aspect=1.33, margin_titles=True)
        grid.map(plot_pie, 'price', 'category')

        filepath = generate_plot_filepath(user_id, plot_type)
        plt.savefig(filepath)

        return filepath

    except Exception as e:
        print(e)
        return BOT_CONFIG['ERROR_IMAGE_FILEPATH']


