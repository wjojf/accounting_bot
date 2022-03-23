import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 
import datetime as dt
from config import BOT_CONFIG


PNG_DIR = BOT_CONFIG['STATIC_PNG_DIR']


def generate_plot_filepath(user_id, plot_type, date_filter):
    return f'{PNG_DIR}{user_id}_{plot_type}_{date_filter})'


def spendings_lineplot_by_date(user_data, plot_date, plot_type='spendings_lineplot_by_date'):

    try:
        currency_grid = sns.FacetGrid(user_data, col='currency', height=3, aspect=1.33, margin_titles=True)
        currency_grid.map(sns.pointplot, 'date', 'price')
        #currency_grid.set_axis_labels(x_var='date', y_var='spent')

        user_id = list(user_data['user_id'])[0]
        plot_filepath = generate_plot_filepath(user_id, plot_type, plot_date)
        plt.savefig(plot_filepath)
        print('Успешно сохранена картинка')
        return plot_filepath

    except Exception as e:
        print(e)
        return BOT_CONFIG['ERROR_IMAGE_FILEPATH']


def spendings_barplot_by_date(user_data, plot_date, plot_type='spendings_barplot_by_date'):
    try:

        fig, ax = plt.subplots(figsize=(9, 9))
        sns.barplot(x='date', y='price', data=user_data, hue='currency', ax=ax)
        plt.xticks(rotation=90)
        plt.xlabel('Дата')
        plt.ylabel('Сумма Затрат')
        plt.title(f'Затраты {list(user_data["user_id"])[0]}')


        user_id = list(user_data['user_id'])[0]
        filepath = generate_plot_filepath(user_id, plot_type, plot_date)
        plt.savefig(filepath)
        print('Успешно сохранена картинка')
        return filepath

    except Exception as e:
        print(e, BOT_CONFIG['ERROR_IMAGE_FILEPATH'])


def categories_barplot_by_currency(user_data, plot_date, plot_type='categoris_barplot_by_currency'):
    try:

        fig, ax = plt.subplots(figsize=(10,10))
        sns.barplot(x='category', y='price', data=user_data, hue='currency', ax=ax)
        plt.xticks(rotation=90)
        plt.xlabel('Дата')
        plt.ylabel('Сумма Затрат')
        plt.title(f'Затраты {list(user_data["user_id"])[0]}')

        user_id = list(user_data['user_id'])[0]
        filepath = generate_plot_filepath(user_id, plot_type, plot_date)
        plt.savefig(filepath)
        print('Успешно сохранена картинка')
        return filepath

    except Exception as e:
        print(e)
        return BOT_CONFIG['ERROR_IMAGE_FILEPATH']


def categories_pieplot_by_currency(user_data, plot_date, plot_type='categories_pieplot_by_currency'):

    def plot_pie(x, labels, **kwargs):
        plt.pie(x=x, labels=labels)

    user_id = list(user_data['user_id'])[0]

    try:
        grid = sns.FacetGrid(user_data, col='currency',height=3, aspect=1.33, margin_titles=True)
        grid.map(plot_pie, 'price', 'category')

        filepath = generate_plot_filepath(user_id, plot_type, plot_date)
        plt.savefig(filepath)

        return filepath

    except Exception as e:
        print(e)
        return BOT_CONFIG['ERROR_IMAGE_FILEPATH']


