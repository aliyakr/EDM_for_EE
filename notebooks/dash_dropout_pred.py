import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import panel as pn
import datetime
import pandas as pd

pn.extension()

# Пример данных для курсов и уровня COR
courses_data = {
    'Курс A': 85,
    'Курс B': 68,
    'Курс C': 92
}

# Функция для построения круговой диаграммы уровня COR
def plot_completion_rate(course_name, completion_rate):
    fig, ax = plt.subplots()
    size = 0.3

    # Создаем градиентный цвет
    cmap = LinearSegmentedColormap.from_list("grad", ["#ff66c4", "#5170ff"])
    colors = [cmap(i / 100) for i in range(100)]

    # Создаем сегменты для градиента
    wedges, texts = ax.pie([1]*100, startangle=90, colors=colors, radius=1, wedgeprops=dict(width=size, edgecolor='w'))
    
    # Создаем белый сегмент для незаполненной части
    ax.pie([completion_rate, 100 - completion_rate], startangle=90, colors=['none', 'white'], radius=1, wedgeprops=dict(width=size, edgecolor='w'))

    # Добавляем текст в центр круга
    ax.text(0, 0, f'{completion_rate:.0f}%', ha='center', va='center', fontsize=43, fontweight='bold', color='#5470fe' if completion_rate != 68 else 'red')
    
    ax.set(aspect="equal", title=f'{course_name} - Уровень доходимости (COR)')
    plt.close(fig)  # Закрыть фигуру для корректного отображения в Panel
    return fig

# Создание графиков для каждого курса
course_plots = [plot_completion_rate(course, rate) for course, rate in courses_data.items()]

# Проблемные модули в виде DataFrame
problem_modules_data = {
    'Модуль': ['Модуль 2', 'Модуль 2'],
    'Задание': ['Задание 3', 'Задание 4'],
    'Проблема': ['Средняя оценка 3.4', 'Длительность выполнения 120 минут']
}
problem_modules_df = pd.DataFrame(problem_modules_data)

# Кнопка для отображения проблемных модулей
problem_button = pn.widgets.Button(name='Проблемы', button_type='danger')

# Функция для отображения информации о проблемных модулях при нажатии кнопки
def show_problems(event):
    problems_pane.object = problem_modules_df

problem_button.on_click(show_problems)

# Панель для отображения проблемных модулей
problems_pane = pn.pane.DataFrame(problem_modules_df, sizing_mode='stretch_width', visible=False)

# Текущая дата
current_date = datetime.date.today().strftime("%Y-%m-%d")

# Отображение графиков и текста с информацией
dashboard = pn.Column(
    "## Прогнозируемый уровень доходимости (COR)",
    f"### Последняя дата обновления: {current_date}",
    pn.Row(
        pn.pane.Matplotlib(course_plots[0], sizing_mode='stretch_width'), 
        pn.Column(pn.pane.Matplotlib(course_plots[1], sizing_mode='stretch_width'), problem_button, problems_pane),
        pn.pane.Matplotlib(course_plots[2], sizing_mode='stretch_width')
    )
)

# Запуск панели
if __name__ == '__main__':
    pn.serve(dashboard)
