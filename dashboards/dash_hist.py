import pandas as pd
import sys
import os
import hvplot.pandas
import holoviews as hv
import panel as pn
from holoviews import opts
from bokeh.models import DatetimeTickFormatter

sys.path.append(os.path.abspath(os.path.join('..', 'scripts')))

hv.extension('bokeh')
pn.extension()

def load_data(file_path):
    return pd.read_csv(file_path)

def create_dashboard():
    try:
        # Загрузка данных
        registration_data = load_data('../data/registration.csv')
        registration_data['дата_отчисление'] = pd.to_datetime(registration_data['дата_отчисление'])

        # Функция для группировки данных по заданному интервалу
        def group_data(data, interval):
            grouped_data = data.set_index('дата_отчисление').resample(interval).size().reset_index(name='count')
            return grouped_data

        # Функция для гистограммы распределения «отсева»
        def plot_dropout_histogram(data, title, interval='D'):
            grouped_data = group_data(data, interval)
            histogram = grouped_data.hvplot.bar(
                x='дата_отчисление', y='count', color="#ff66c4", title=title, 
                xlabel='Дата отчисления', ylabel='Количество студентов'
            ).opts(
                opts.Bars(line_color='white', line_width=1, show_grid=False)
            )
            bokeh_plot = hv.render(histogram, backend='bokeh')
            bokeh_plot.xaxis.major_label_orientation = 1.5708  # Установка угла 90 градусов (в радианах)
            bokeh_plot.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m", months="%Y-%m", years="%Y-%m")
            return bokeh_plot

        # Инициализация выпадающего списка
        intervals = {'Дни': 'D', 'Недели': 'W', 'Месяцы': 'M', 'Годы': 'Y'}
        interval_dropdown = pn.widgets.Select(name='Группировать по', options=list(intervals.keys()), value='Дни')

        # Функция для обновления графика при изменении выпадающего списка
        @pn.depends(interval_dropdown.param.value)
        def update_histogram(interval):
            interval_value = intervals[interval]
            return plot_dropout_histogram(registration_data, 'Гистограмма распределения отсева', interval_value)

        # Создание макета
        layout = pn.Column(interval_dropdown, pn.panel(update_histogram))

        return layout

    except KeyboardInterrupt:
        print("Программа была прервана пользователем.")
    except Exception as e:
        print(e)
        sys.exit()

# Запуск дашборда
dashboard = create_dashboard()
dashboard.servable()













