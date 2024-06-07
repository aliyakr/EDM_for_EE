import pandas as pd
import hvplot.pandas
import panel as pn

# Загрузка данных
students_materials_data = pd.read_csv('../data/students_materials.csv')
students_materials_data['дата'] = pd.to_datetime(students_materials_data['дата'])

# Гистограмма распределения времени на каждом материале
def plot_material_time_histogram(data, title):
    return data['длительность_пребывания'].hvplot.hist(
        bins=30,
        xlabel='Длительность пребывания (минуты)',
        ylabel='Количество посещений',
        title=title,
        width=600,
        height=400
    )

# График плотности времени на каждом материале
def plot_material_time_density(data, title):
    return data['длительность_пребывания'].hvplot.kde(
        xlabel='Длительность пребывания (минуты)',
        ylabel='Плотность',
        title=title,
        width=600,
        height=400
    )

# Граф активности
def plot_activity_graph(data, title):
    return data.hvplot.hist(
        x='дата',
        by='код_материал',
        bins=30,
        xlabel='Дата',
        ylabel='Количество посещений',
        title=title,
        width=600,
        height=400,
        legend='top'
    )

# Создание дэшборда
pn.extension()

histogram = plot_material_time_histogram(students_materials_data, 'Распределение времени на каждом материале')
density = plot_material_time_density(students_materials_data, 'Плотность времени на каждом материале')
activity = plot_activity_graph(students_materials_data, 'Активность по материалам')

dashboard = pn.Column(
    pn.pane.Markdown("# Анализ взаимодействия с материалами"),
    pn.Row(histogram, density),
    activity
)

dashboard.show()



