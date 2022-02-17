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



def generate_df_from_db_rows(db_rows, column_names):
    return pd.DataFrame(db_rows, columns=column_names)


def filter_df_by_date(user_df, date_min, date_max):
    
    try:
        return user_df[(user_df['date'] >= date_min) & (user_df['date'] <= date_max)]
    
    except: 
        return None
'''user_data: df of columns ['user_id', date', 'currency', 'money_spent']'''
def spendings_barplot_by_date(user_data, plot_type='spendings_barplot_by_date'):
    try:
        sns.barplot(x='date', y='money_spent', data=user_data, hue='currency')
        plt.xticks(rotation=90)
        plt.xlabel('Дата')
        plt.ylabel('Сумма Затрат')
        plt.title(f'Затраты {list(user_data["user_id"])[0]}')

        filepath = generate_plot_filepath(list(user_data['user_id'])[0], plot_type)
        plt.savefig(filepath)
        print('Успешно сохранена картинка')
        return filepath

    except Exception as e:
        print(e, BOT_CONFIG['ERROR_IMAGE_FILEPATH'])


def categories_pieplot_by_currency(user_data, plot_type='category_spendings_pieplot'):
    '''user_data: df of columns ['user_id', 'category', 'money_spent', 'currency']'''
    def plot_pie(x, labels, **kwargs):
        plt.pie(x=x, labels=labels)

    try:
        grid = sns.FacetGrid(user_data, col='currency')
        grid.map(plot_pie, 'money_spent','category')
        
        filepath = generate_plot_filepath(list(user_data['user_id'])[0], plot_type)
        plt.savefig(filepath)
        return filepath
    
    except:
        return BOT_CONFIG['ERROR_IMAGE_FILEPATH']

def category_lineplot_by_date(user_data, plot_type='category_lineplot_by_date'):
    '''user_data: df of columns ['user_id','category', 'currency', date', 'money_spent']'''
    category = list(user_data['category'])[0]
    user_id = list(user_data['user_id'])[0]

    try:
        grid = sns.FacetGrid(user_data, col='currency')
        grid.map(sns.lineplot, x='date', y='money_spent')

        plt.xlabel('Дата')
        plt.ylabel('Затраты')
        plt.title(f'Затраты в категории {category}')

        filepath = generate_plot_filepath(user_id, plot_type)
    except:
        return BOT_CONFIG['ERROR_IMAGE_FILEPATH']


def categories_barplot_by_currency(user_data, plot_type='categoris_barplot_by_currency'):
    '''user_data: df of columns ['user_id', 'category', 'currency', 'money_spent']'''

    user_id = list(use_data['user_id'])[0]
    user_data.drop(columns=['user_id'], inplace=True)

    try:
        grid = sns.FacetGrid(user_data, col='currency')
        grid.map(sns.catplot, x='category', y='money_spent', kind='bar')

        filepath = generate_plot_filepath(user_id, plot_type)
        plt.savefig(filepath)

        return filepath

    except:
        return BOT_CONFIG['ERROR_IMAGE_FILEPATH']

