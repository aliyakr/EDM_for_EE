import pandas as pd
import numpy as np
import panel as pn
import hvplot.pandas

# Генерация тестовых данных
np.random.seed(0)

# Данные материалов
materials = pd.DataFrame({
    'код_сотрудник': np.random.randint(1, 101, 1000),
    'код_материал': np.random.randint(1, 21, 1000),  # коды материалов от 1 до 20
    'длительность_пребывания': np.random.uniform(5, 60, 1000)
})

# Функции анализа взаимодействия с материалами
def section_visit_frequency(data):
    section_visits = data['код_материал'].value_counts().sort_index()
    return section_visits

def average_time_per_section(data):
    avg_time = data.groupby('код_материал')['длительность_пребывания'].mean().sort_index()
    return avg_time

def section_popularity(data):
    total_visits = data['код_материал'].count()
    popularity = (data['код_материал'].value_counts().sort_index() / total_visits) * 100
    return popularity

# Вызов функций
section_visits = section_visit_frequency(materials)
avg_time_section = average_time_per_section(materials)
popularity = section_popularity(materials)

# Создание дэшборда
pn.extension('hvplot')

# Цветовая гамма
color_palette = '#5470fe'

# Функция для создания графиков
def create_section_visit_plot():
    data = section_visits.reset_index()
    data.columns = ['Код материала', 'Частота посещений']
    return data.hvplot.bar(x='Код материала', y='Частота посещений', color=color_palette, title='Частота посещений разделов')

def create_avg_time_plot():
    data = avg_time_section.reset_index()
    data.columns = ['Код материала', 'Среднее время пребывания']
    return data.hvplot.bar(x='Код материала', y='Среднее время пребывания', color=color_palette, title='Среднее время пребывания на каждом разделе')

def create_popularity_plot():
    data = popularity.reset_index()
    data.columns = ['Код материала', 'Популярность (%)']
    return data.hvplot.bar(x='Код материала', y='Популярность (%)', color=color_palette, title='Популярность разделов')

# Создание графиков
section_visit_plot = create_section_visit_plot()
avg_time_plot = create_avg_time_plot()
popularity_plot = create_popularity_plot()

# Организация дэшборда
dashboard = pn.Column(
    '## Анализ взаимодействия с материалами',
    section_visit_plot,
    avg_time_plot,
    popularity_plot
)

dashboard.servable()
