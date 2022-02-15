import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 
from config import BOT_CONFIG


def get_plot_spendings__image_by_date(user_data):
	'''user_data: df of columns ['user_id', date', 'currency', 'money_spent']'''
	try:
		sns.barplot(x='date', y='money_spent', data=user_data, hue='currency')
		plt.xlabel('Дата')
		plt.ylabel('Сумма Затрат')
		plt.title(f'Затраты за период {user_data['date'].min()}-{user_data['date'].max()}')
		
		filepath = generate_plot_title(list(user_data['user_id'])[0], 'spendings_by_date', user_data['date'].min(), user_data['date'].max())
		plt.savefig(filepath)
		print('Успешно сохранена картинка')
		return filepath
	except:
		 print('Ошибка данных')
		 return BOT_CONFIG['ERROR_IMAGE_FILEPATH']

