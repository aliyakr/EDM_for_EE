import pandas as pd
import numpy as np
import hvplot.pandas
import holoviews as hv
import panel as pn
from holoviews import opts
from bokeh.models import DatetimeTickFormatter

hv.extension('bokeh')
pn.extension()

# Создание псевдоданных
def create_fake_data():
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    num_entries = len(dates)
    
    # Генерация данных регистрации и отчисления с некоторым паттерном
    registration_counts = np.random.poisson(lam=5, size=num_entries)
    dismissal_counts = np.random.poisson(lam=3, size=num_entries)
    
    registration_data = pd.DataFrame({
        'дата_регистрация': dates,
        'количество_регистраций': registration_counts
    })
    
    dismissal_data = pd.DataFrame({
        'дата_отчисление': dates,
        'количество_отчислений': dismissal_counts
    })
    
    return registration_data, dismissal_data

# Функция для анализа временных паттернов
def time_pattern_analysis(reg_data, dis_data):
    reg_data['дата_регистрация'] = pd.to_datetime(reg_data['дата_регистрация'], errors='coerce')
    dis_data['дата_отчисление'] = pd.to_datetime(dis_data['дата_отчисление'], errors='coerce')
    
    reg_data = reg_data.dropna(subset=['дата_регистрация'])
    dis_data = dis_data.dropna(subset=['дата_отчисление'])
    
    weekly_registration = reg_data.set_index('дата_регистрация').resample('W').sum().reset_index()
    weekly_dismissal = dis_data.set_index('дата_отчисление').resample('W').sum().reset_index()
    
    return weekly_registration, weekly_dismissal

def create_dashboard():
    try:
        # Создание псевдоданных
        registration_data, dismissal_data = create_fake_data()

        # Анализ временных паттернов
        weekly_registration, weekly_dismissal = time_pattern_analysis(registration_data, dismissal_data)

        # Функция для создания интерактивного графика
        def plot_time_patterns(reg_data, dis_data, title):
            reg_plot = reg_data.hvplot.line(
                x='дата_регистрация', y='количество_регистраций', color="#5170ff", label='Регистрация',
                xlabel='Дата', ylabel='Количество студентов'
            )
            dis_plot = dis_data.hvplot.line(
                x='дата_отчисление', y='количество_отчислений', color="#ff66c4", label='Отчисление',
                xlabel='Дата', ylabel='Количество студентов'
            )
            combined_plot = reg_plot * dis_plot
            combined_plot.opts(
                title=title,
                legend_position='top_left',
                xrotation=90,
                width=800,
                height=400
            )
            bokeh_plot = hv.render(combined_plot, backend='bokeh')
            bokeh_plot.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d", months="%Y-%m", years="%Y-%m")
            bokeh_plot.xgrid.grid_line_color = None  # Удаление сетки
            bokeh_plot.ygrid.grid_line_color = None
            return bokeh_plot

        # Инициализация выпадающего списка
        intervals = {'Дни': 'D', 'Недели': 'W', 'Месяцы': 'ME', 'Годы': 'YE'}
        interval_dropdown = pn.widgets.Select(name='Группировать по', options=list(intervals.keys()), value='Недели')

        # Функция для обновления графиков при изменении выпадающего списка
        @pn.depends(interval_dropdown.param.value)
        def update_plots(interval):
            interval_value = intervals[interval]
            grouped_registration = registration_data.set_index('дата_регистрация').resample(interval_value).sum().reset_index()
            grouped_dismissal = dismissal_data.set_index('дата_отчисление').resample(interval_value).sum().reset_index()
            
            plot = plot_time_patterns(grouped_registration, grouped_dismissal, 'Временные паттерны регистрации и отчисления студентов')
            return plot

        # Создание макета
        layout = pn.Column(interval_dropdown, pn.panel(update_plots))

        return layout

    except KeyboardInterrupt:
        print("Программа была прервана пользователем.")
    except Exception as e:
        print(e)
        sys.exit()

# Запуск дашборда
dashboard = create_dashboard()
dashboard.servable()


