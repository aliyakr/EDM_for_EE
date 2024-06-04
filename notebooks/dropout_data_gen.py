import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker('ru_RU')

# Параметры
num_students = 1000
num_courses = 3
num_modules_per_course = 10
num_materials_per_module = 5
num_assignments_per_module = 5

# Генерация данных
students = [f'студент_{i+1}' for i in range(num_students)]
statuses = ['прошел курс', 'не закончил']
courses = [f'курс_{i+1}' for i in range(num_courses)]
modules = [f'модуль_{i+1}' for i in range(num_modules_per_course)]
materials = [f'материал_{i+1}' for i in range(num_materials_per_module)]
assignments = [f'задание_{i+1}' for i in range(num_assignments_per_module)]

# Создание DataFrame для студентов
students_info = pd.DataFrame({
    'код_сотрудник': students,
    'возраст': np.random.randint(20, 60, num_students),
    'опыт_работы': np.random.randint(1, 30, num_students),
    'отдел': np.random.choice(['Отдел производства', 'Отдел качества', 'Отдел закупок', 'Отдел продаж', 'Отдел IT', 'Отдел кадров'], num_students),
    'должность': np.random.choice(['Рабочий', 'Инженер', 'Мастер', 'Техник', 'Начальник смены', 'Контролер', 'Инспектор', 'Техник по качеству', 'Начальник отдела', 'Менеджер по качеству'], num_students),
    'статус': np.random.choice(statuses, num_students, p=[0.5, 0.5]),
    'оценка_итог': np.random.randint(50, 100, num_students)
})

# Создание DataFrame для активности студентов
activity_data = []
for student in students:
    for course in courses:
        for module in modules:
            for material in materials:
                if random.random() > 0.3:
                    activity_data.append({
                        'код_сотрудник': student,
                        'код_курс': course,
                        'код_модуль': module,
                        'код_материал': material,
                        'дата': fake.date_between(start_date='-1y', end_date='today'),
                        'длительность_пребывания': random.randint(1, 120)
                    })
activity_df = pd.DataFrame(activity_data)

# Создание DataFrame для заданий студентов
assignments_data = []
for student in students:
    for course in courses:
        for module in modules:
            for assignment in assignments:
                if random.random() > 0.3:
                    assignments_data.append({
                        'код_сотрудник': student,
                        'код_курс': course,
                        'код_модуль': module,
                        'код_задание': assignment,
                        'дата_выполнения': fake.date_between(start_date='-1y', end_date='today'),
                        'оценка': random.randint(50, 100),
                        'попытка': random.randint(1, 3)
                    })
assignments_df = pd.DataFrame(assignments_data)

# Сохранение данных в CSV
students_info.to_csv('processed_students_info.csv', index=False)
activity_df.to_csv('processed_students_activity.csv', index=False)
assignments_df.to_csv('processed_students_assignments.csv', index=False)

