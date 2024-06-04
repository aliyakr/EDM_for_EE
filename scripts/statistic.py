import pandas as pd
from scipy import stats
import numpy as np

# Диагностика входных данных
def data_diagnostics(data):
    diagnostics = {
        'mean': data.select_dtypes(include=[np.number]).mean(),
        'median': data.select_dtypes(include=[np.number]).median(),
        'std': data.select_dtypes(include=[np.number]).std(),
        'min': data.select_dtypes(include=[np.number]).min(),
        'max': data.select_dtypes(include=[np.number]).max()
    }
    return diagnostics

# Расчет уровня доходимости
def calculate_completion_rate(data):
    completion_rate = (data['статус'] == 'прошел курс').mean() * 100
    return completion_rate

# Выявление временных паттернов
def time_pattern_analysis(data):
    # Преобразование данных в datetime
    data['дата_регистрация'] = pd.to_datetime(data['дата_регистрация'], errors='coerce')
    data['дата_отчисление'] = pd.to_datetime(data['дата_отчисление'], errors='coerce')
    
    # Фильтрация данных для удаления некорректных дат
    data = data.dropna(subset=['дата_регистрация', 'дата_отчисление'])
    
    # Ресемплирование данных по неделям
    weekly_registration = data.set_index('дата_регистрация').resample('W').size()
    weekly_dismissal = data.set_index('дата_отчисление').resample('W').size()
    
    return weekly_registration, weekly_dismissal


# Сравнительный анализ характеристик
def compare_groups(data, group_col, value_col):
    groups = data.groupby(group_col)[value_col]
    group_keys = list(groups.groups.keys())
    return stats.ttest_ind(groups.get_group(group_keys[0]), groups.get_group(group_keys[1]))

# Частота посещений разделов
def section_visit_frequency(data):
    section_visits = data['код_материал'].value_counts()
    return section_visits

# Среднее время, проведенное на каждом разделе
def average_time_per_section(data):
    avg_time = data.groupby('код_материал')['длительность_пребывания'].mean()
    return avg_time

# Популярность разделов
def section_popularity(data):
    total_visits = data['код_материал'].count()
    popularity = (data['код_материал'].value_counts() / total_visits) * 100
    return popularity

# Оценка когнитивной посильности
def cognitive_load_assessment(assignments_data, students_info):
    # Проверка наличия необходимых столбцов
    required_columns = ['код_задание', 'оценка', 'попытка']
    if not all(col in assignments_data.columns for col in required_columns):
        raise KeyError(f"Необходимые столбцы отсутствуют в данных assignments_data: {', '.join(required_columns)}")

    required_student_columns = ['код_курс', 'оценка_итог']
    if not all(col in students_info.columns for col in required_student_columns):
        raise KeyError(f"Необходимые столбцы отсутствуют в данных students_info: {', '.join(required_student_columns)}")

    # Сложность задания
    complexity = assignments_data.groupby('код_задание').apply(lambda x: (x['оценка'] >= 50).mean())

    # Дискриминативность задания
    def discriminative_power(x):
        group_means = students_info.groupby('код_курс')['оценка_итог'].mean()
        return group_means.max() - group_means.min()
    
    discriminativity = assignments_data.groupby('код_задание').apply(discriminative_power)
    
    # Индекс попытки
    attempt_index = assignments_data.groupby('код_задание')['попытка'].mean().apply(lambda x: 1 / x)
    
    # Оценка когнитивной посильности
    cognitive_load = (complexity + discriminativity + attempt_index) / 3
    
    return cognitive_load

# Формирование итогового датасета для анализа
def create_final_dataset(students_info, assignments, materials):
    # Средняя оценка за все задания
    avg_score = assignments.groupby('код_сотрудник')['оценка'].mean().reset_index()
    avg_score.columns = ['код_сотрудник', 'средняя_оценка']

    # Количество завершенных заданий
    completed_assignments = assignments.groupby('код_сотрудник')['код_задание'].count().reset_index()
    completed_assignments.columns = ['код_сотрудник', 'количество_завершенных_заданий']

    # Среднее время на материал
    avg_time_material = materials.groupby('код_сотрудник')['длительность_пребывания'].mean().reset_index()
    avg_time_material.columns = ['код_сотрудник', 'среднее_время_на_материале']

    # Объединение данных
    final_data = students_info.merge(avg_score, on='код_сотрудник', how='left')
    final_data = final_data.merge(completed_assignments, on='код_сотрудник', how='left')
    final_data = final_data.merge(avg_time_material, on='код_сотрудник', how='left')

    # Заполнение пропусков
    final_data = final_data.fillna(0)

    return final_data

if __name__ == "__main__":
    # Загрузка данных для первой задачи
    registration_data = pd.read_csv('../data/registration.csv')
    students_info_data = pd.read_csv('../data/students_info.csv')
    
    # Диагностика входных данных
    diagnostics = data_diagnostics(registration_data)
    print("Диагностика:", diagnostics)

    # Расчет уровня доходимости
    completion_rate = calculate_completion_rate(students_info_data)
    print("Уровень доходимости:", completion_rate)

    # Выявление временных паттернов
    time_patterns = time_pattern_analysis(registration_data)
    print("Временные паттерны:", time_patterns)

    # Сравнительный анализ характеристик
    comparison = compare_groups(students_info_data, 'отдел', 'оценка_итог')
    print("Сравнение характеристик:", comparison)
    
    # Загрузка данных для второй задачи
    students_materials_data = pd.read_csv('../data/students_materials.csv')
    students_assignments_data = pd.read_csv('../data/students_assignments.csv')

    # Частота посещений разделов
    visit_frequency = section_visit_frequency(students_materials_data)
    print("Частота посещений разделов:", visit_frequency)

    # Среднее время, проведенное на каждом разделе
    avg_time = average_time_per_section(students_materials_data)
    print("Среднее время по разделам:", avg_time)

    # Популярность разделов
    popularity = section_popularity(students_materials_data)
    print("Популярность разделов:", popularity)

    # Оценка когнитивной посильности
    cognitive_load = cognitive_load_assessment(students_assignments_data, students_info_data)
    print("Оценка когнитивной посильности:", cognitive_load)

    # Создание итогового датасета для анализа
    final_dataset = create_final_dataset(students_info_data, students_assignments_data, students_materials_data)
    final_dataset.to_csv('../data/final_dataset.csv', index=False)
    print("Итоговый датасет сохранен в '../data/final_dataset.csv'.")




