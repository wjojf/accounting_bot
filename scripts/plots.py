import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 
import datetime as dt
from config import BOT_CONFIG


PNG_DIR = BOT_CONFIG['STATIC_PNG_DIR']

def generate_plot_filepath(user_id, plot_type,date_min=None, date_max=None):
    
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



def generate_df_from_db_rows(column_names, db_rows):
    return pd.DataFrame(db_rows, columns=column_names)


def filter_df_by_date(user_df, date_min, date_max):
    
    try:
        return user_df[(user_df['date'] >= date_min) & (user_df['date'] <= date_max)]
    
    except: 
        return None 
 
def spendings_barplot_by_date(user_data, plot_type='spendings_barplot_by_date'):
	'''user_data: df of columns ['user_id', date', 'currency', 'money_spent']'''
	try:
		sns.barplot(x='date', y='money_spent', data=user_data, hue='currency')
		plt.xlabel('Дата')
		plt.ylabel('Сумма Затрат')
		plt.title(f'Затраты за период {user_data["date"].min()}-{user_data["date"].max()}')
		
		filepath = generate_plot_filepath(
      			list(user_data['user_id'])[0],
         		plot_type,
           		user_data['date'].min(),
             	user_data['date'].max())
		plt.savefig(filepath)
		print('Успешно сохранена картинка')
		return filepath
	
	except:
		print('Ошибка данных')
		return BOT_CONFIG['ERROR_IMAGE_FILEPATH']


def category_pieplot_by_currency(user_data, plot_type='category_spendings_pieplot'):
    '''user_data: df of columns ['user_id', 'category', 'money_spent', 'currency']'''
    def plot_pie(x, labels, **kwargs):
        plt.pie(x=x, labels=labels)

    try:
        grid = sns.FacetGrid(user_data, col='currency')
        grid.map(plot_pie, 'money_spent','category')
        
        filepath = generate_plot_filepath(list(user_data['user_id'])[0], plot_type)
        plt.savefig(filepath)
    
    except:
        return BOT_CONFIG['ERROR_IMAGE_FILEPATH']
