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
    num_students = 1000
    departments = ['Отдел производства', 'Отдел качества', 'Отдел закупок', 'Отдел продаж', 'Отдел IT', 'Отдел кадров']
    positions = ['Рабочий', 'Инженер', 'Мастер', 'Техник', 'Начальник смены', 'Контролер', 'Инспектор', 'Техник по качеству', 'Начальник отдела', 'Менеджер по качеству', 'Специалист по закупкам', 'Менеджер по снабжению', 'Аналитик', 'Логист', 'Кладовщик', 'Менеджер по продажам', 'Специалист по рекламе', 'Консультант', 'Торговый представитель', 'Аналитик продаж', 'Программист', 'Системный администратор', 'Инженер по безопасности', 'Техник поддержки', 'Начальник отдела', 'Рекрутер', 'HR-менеджер', 'Инспектор по кадрам', 'Специалист по обучению', 'Начальник отдела']
    
    data = pd.DataFrame({
        'код_сотрудник': [f'студент_{i+1}' for i in range(num_students)],
        'возраст': np.random.randint(20, 60, num_students),
        'опыт_работы': np.random.randint(1, 30, num_students),
        'отдел': np.random.choice(departments, num_students),
        'должность': np.random.choice(positions, num_students),
        'оценка_итог': np.random.randint(50, 100, num_students)
    })
    
    return data

# Функция для сравнительного анализа характеристик
def compare_groups(data, group_col, value_col):
    groups = data.groupby(group_col)[value_col]
    group_stats = groups.describe()
    return group_stats

def create_comparison_dashboard():
    try:
        # Создание псевдоданных
        student_data = create_fake_data()

        # Инициализация выпадающего списка для группировки и характеристики
        group_cols = ['отдел', 'должность']
        value_cols = ['возраст', 'опыт_работы', 'оценка_итог']
        
        group_col_dropdown = pn.widgets.Select(name='Группировать по', options=group_cols, value='отдел')
        value_col_dropdown = pn.widgets.Select(name='Характеристика', options=value_cols, value='возраст')

        # Функция для обновления графиков при изменении выпадающего списка
        @pn.depends(group_col_dropdown.param.value, value_col_dropdown.param.value)
        def update_plots(group_col, value_col):
            group_stats = compare_groups(student_data, group_col, value_col)
            bars = group_stats['mean'].hvplot.bar(
                title=f'Сравнительный анализ {value_col} по {group_col}',
                xlabel=group_col.capitalize(),
                ylabel=f'Среднее значение {value_col}',
                color='#ff66c4'
            ).opts(
                opts.Bars(line_color='white', line_width=1, xrotation=45, width=800, height=400)
            )
            return bars

        # Создание макета
        layout = pn.Column(group_col_dropdown, value_col_dropdown, pn.panel(update_plots))

        return layout

    except KeyboardInterrupt:
        print("Программа была прервана пользователем.")
    except Exception as e:
        print(e)
        sys.exit()

# Запуск дашборда
dashboard = create_comparison_dashboard()
dashboard.servable()
