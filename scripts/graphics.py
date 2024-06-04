import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Гистограмма распределения «отсева»
def plot_dropout_histogram(data, title):
    plt.figure(figsize=(10, 6))
    data['дата_отчисление'] = pd.to_datetime(data['дата_отчисление'])
    plt.hist(data['дата_отчисление'], bins=30, color="#ff66c4", edgecolor='black')
    plt.title(title)
    plt.xlabel('Дата отчисления')
    plt.ylabel('Количество студентов')
    plt.grid(axis='y', alpha=0.75)
    plt.show()

# Линейный график «отсева»
def plot_dropout_line(data, title):
    plt.figure(figsize=(10, 6))
    data['дата_отчисление'] = pd.to_datetime(data['дата_отчисление'])
    dropout_counts = data['дата_отчисление'].value_counts().sort_index()
    plt.plot(dropout_counts.index, dropout_counts.values, color="#5170ff", marker='o')
    plt.title(title)
    plt.xlabel('Дата отчисления')
    plt.ylabel('Количество студентов')
    plt.grid(axis='both', alpha=0.75)
    plt.show()

# Корреляционный анализ важности признаков
def plot_correlation_matrix(data, title, method='pearson'):
    plt.figure(figsize=(12, 10))
    correlation_matrix = data.corr(method=method)
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, cbar_kws={'shrink': .8})
    plt.title(f'{title} (method={method})')
    plt.show()

# Гистограмма распределения времени на каждом материале
def plot_material_time_histogram(data, title):
    plt.figure(figsize=(10, 6))
    data['длительность_пребывания'].hist(bins=30)
    plt.title(title)
    plt.xlabel('Длительность пребывания (минуты)')
    plt.ylabel('Количество посещений')
    plt.show()

# График плотности времени на каждом материале
def plot_material_time_density(data, title):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data['длительность_пребывания'])
    plt.title(title)
    plt.xlabel('Длительность пребывания (минуты)')
    plt.ylabel('Плотность')
    plt.show()

# Граф активности
def plot_activity_graph(data, title):
    plt.figure(figsize=(10, 6))
    sns.histplot(data, x='дата', hue='код_материал', multiple='stack')
    plt.title(title)
    plt.xlabel('Дата')
    plt.ylabel('Количество посещений')
    plt.show()

if __name__ == "__main__":
    # Загрузка данных для первой задачи
    registration_data = pd.read_csv('data/processed_registration.csv')
    students_info_data = pd.read_csv('data/processed_students_info.csv')
    
    # Гистограмма распределения «отсева»
    plot_dropout_histogram(students_info_data, 'Гистограмма распределения отсева студентов')

    # Линейный график «отсева»
    plot_dropout_line(students_info_data, 'Линейный график отсева студентов')

    # Корреляционный анализ важности признаков (Пирсон)
    plot_correlation_matrix(students_info_data, 'Корреляционный анализ важности признаков (Пирсон)', method='pearson')

    # Корреляционный анализ важности признаков (Спирмен)
    plot_correlation_matrix(students_info_data, 'Корреляционный анализ важности признаков (Спирмен)', method='spearman')
    
    # Загрузка данных для второй задачи
    students_materials_data = pd.read_csv('data/processed_students_materials.csv')

    # Гистограмма распределения времени на каждом материале
    plot_material_time_histogram(students_materials_data, 'Гистограмма времени пребывания на материалах')

    # График плотности времени на каждом материале
    plot_material_time_density(students_materials_data, 'График плотности времени пребывания на материалах')

    # Граф активности
    students_materials_data['дата'] = pd.to_datetime(students_materials_data['дата'])
    plot_activity_graph(students_materials_data, 'Граф активности по материалам')
