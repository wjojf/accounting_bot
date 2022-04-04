import matplotlib.pyplot as plt
import seaborn as sns
from config import BOT_CONFIG
import DataFrames as dfr


PNG_DIR = BOT_CONFIG['STATIC_PNG_DIR']


def generate_plot_filepath(user_id, plot_type, date_filter, currency):
    return f'{PNG_DIR}{user_id}_{plot_type}_{date_filter}_{currency}.png'


def getXticks(pd_series):
    mid = dfr.objectSeriesMid(pd_series)
    return [
        val
        if val == pd_series.min()
        or val == pd_series.max()
        or val in mid
        else ''
        for val in pd_series
    ]


def generate_plot_title(user_alias, plot_date):
    plot_date_text = {
        "today": "Сегодня",
        "this_week": "Эта неделя",
        "this_month": "Этот месяц",
        "three_months": "Последние три месяца",
        "six_months": "Последние полгода",
        "this_year": "Этот год"
    }

    try:
        return f'Затраты {user_alias} {plot_date_text[plot_date]}'
    except KeyError:
        return f'Затраты {user_alias}'


def spendings_lineplot_by_date(user_data, plot_date, plot_type='spendings_lineplot_by_date'):

    try:
        plt.style.use(['dark_background'])
        user_id = list(user_data['user_id'])[0]
        user_data.sort_values(by='date', inplace=True)

        plots_filepath = []

        for currency in user_data['currency'].unique():
            currency_df = user_data[user_data['currency'] == currency]

            fig, ax = plt.subplots()
            plot_filepath = generate_plot_filepath(user_id, plot_type, plot_date, currency)
            plot_title = generate_plot_title(user_id, plot_date)

            ax.set_title(plot_title)
            sns.lineplot(data=currency_df, x='date', y='price', label=currency)

            ax.set_xlabel('Дата')
            ax.set_ylabel('Потрачено')

            xticks = getXticks(currency_df['date'])
            ax.axes.xaxis.set_ticklabels(xticks)

            ax.legend()

            fig.tight_layout()
            fig.savefig(plot_filepath)
            plt.close(fig)

            plots_filepath.append(plot_filepath)

        return plots_filepath if len(plots_filepath) > 1 else plots_filepath[0]

    except Exception as e:
        print(e)
        return BOT_CONFIG['ERROR_IMAGE_FILEPATH']


def spendings_barplot_by_date(user_data, plot_date, plot_type='spendings_barplot_by_date'):

    try:
        plt.style.use(['dark_background'])
        user_id = list(user_data['user_id'])[0]
        plot_title = generate_plot_title(user_id, plot_date)

        plots = []

        for currency in user_data['currency'].unique():
            currency_df = user_data[user_data['currency'] == currency].copy()
            currency_df = currency_df.groupby(['user_id', 'date']).agg({'price': "sum"}).reset_index()
            currency_df.sort_values(by='date', inplace=True)

            plot_filepath = generate_plot_filepath(user_id, plot_type, plot_date, currency)

            fig, ax = plt.subplots()

            sns.barplot(data=currency_df, x='date', y='price', ax=ax, label=currency)
            ax.set_title(plot_title)
            ax.set_xlabel('Дата')
            ax.set_ylabel('Потрачено')
            xticks = getXticks(currency_df['date'])
            ax.axes.xaxis.set_ticklabels(xticks)
            ax.legend()

            fig.tight_layout()
            fig.savefig(plot_filepath)
            plots.append(plot_filepath)

            plt.close(fig)

        return plots

    except Exception as e:
        print(e)
        return BOT_CONFIG['ERROR_IMAGE_FILEPATH']


def categories_barplot_by_currency(user_data, plot_date, plot_type='categoris_barplot_by_currency'):

    try:
        plt.style.use(['dark_background'])
        user_id = list(user_data['user_id'])[0]
        plot_title = generate_plot_title(user_id, plot_date)

        plots = []

        for currency in user_data['currency'].unique():
            currency_df = user_data[user_data['currency'] == currency].copy()
            currency_df = currency_df.groupby(['user_id', 'category']).agg({'price': 'sum'}).reset_index()

            fig, ax = plt.subplots()

            sns.barplot(data=currency_df, x='category', y='price', ax=ax, label=currency)

            ax.set_xlabel('Категория')
            ax.set_ylabel('Потрачено')
            ax.tick_params(axis='x', labelrotation=45)
            ax.set_title(plot_title)
            ax.legend()

            plot_filepath = generate_plot_filepath(user_id, plot_type, plot_date, currency)

            fig.tight_layout()
            fig.savefig(plot_filepath)
            plots.append(plot_filepath)

            plt.close(fig)

        return plots

    except Exception as e:
        print(e)
        return BOT_CONFIG['ERROR_IMAGE_FILEPATH']


def categories_pieplot_by_currency(user_data, plot_date, plot_type='categories_pieplot_by_currency'):
    return BOT_CONFIG['ERROR_IMAGE_FILEPATH']

