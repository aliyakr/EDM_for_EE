import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker('ru_RU')

# Параметры
num_courses = 3
num_modules_per_course = 10
num_students_per_course = 200
start_date = pd.to_datetime('2023-01-01')

# Генерация кодов курсов и модулей
courses = [f"курс_{i+1}" for i in range(num_courses)]
modules = {course: [f"модуль_{i+1}" for i in range(num_modules_per_course)] for course in courses}
students = {course: [f"студент_{i+1}" for i in range(num_students_per_course)] for course in courses}

# Отделы и должности
departments = {
    'Отдел производства': ['Рабочий', 'Инженер', 'Мастер', 'Техник', 'Начальник смены'],
    'Отдел качества': ['Контролер', 'Инспектор', 'Техник по качеству', 'Начальник отдела', 'Менеджер по качеству'],
    'Отдел закупок': ['Специалист по закупкам', 'Менеджер по снабжению', 'Аналитик', 'Логист', 'Кладовщик'],
    'Отдел продаж': ['Менеджер по продажам', 'Специалист по рекламе', 'Консультант', 'Торговый представитель', 'Аналитик продаж'],
    'Отдел IT': ['Программист', 'Системный администратор', 'Инженер по безопасности', 'Техник поддержки', 'Начальник отдела'],
    'Отдел кадров': ['Рекрутер', 'HR-менеджер', 'Инспектор по кадрам', 'Специалист по обучению', 'Начальник отдела']
}

# Список отзывов
positive_reviews = [
    "Отличный курс, много полезной информации.",
    "Преподаватели супер, материал изложен доступно.",
    "Очень понравилось, буду рекомендовать коллегам.",
    "Курс превзошел мои ожидания, узнал много нового.",
    "Отличная организация учебного процесса.",
    "Много практических занятий, что очень полезно.",
    "Материалы курса на высшем уровне.",
    "Очень хорошие учебные материалы.",
    "Замечательный курс, все четко и по делу.",
    "Преподаватели дают много полезных советов."
]

neutral_reviews = [
    "Курс хороший, но можно было бы добавить больше практики.",
    "Материал неплохой, но иногда скучновато.",
    "Неплохо, но можно было бы улучшить организацию.",
    "Достаточно информативно, но не хватило времени на практику.",
    "Средний курс, ожидал немного большего.",
    "Учебные материалы хорошие, но местами не хватало примеров.",
    "Нормально, но хотелось бы больше интерактива.",
    "Курс неплохой, но слишком много теории.",
    "В целом неплохо, но есть куда расти.",
    "Материалы курса иногда тяжело воспринимаются."
]

negative_reviews = [
    "Не понравился курс, материал плохо подан.",
    "Очень скучно, мало полезной информации.",
    "Преподаватели не смогли заинтересовать.",
    "Материалы устарели, нуждаются в обновлении.",
    "Курс не оправдал ожиданий.",
    "Организация учебного процесса оставляет желать лучшего.",
    "Слишком много теории, мало практики.",
    "Материалы курса плохо структурированы.",
    "Преподаватели не отвечают на вопросы.",
    "Очень разочарован, зря потратил время."
]

all_reviews = positive_reviews + neutral_reviews + negative_reviews

def random_date(start, end):
    return fake.date_between(start, end)

def add_seasonal_effects(date):
    month = date.month
    if month in [1, 2, 9, 10]:  # начало и конец учебного года
        return np.random.normal(loc=1.5, scale=0.5)
    else:
        return np.random.normal(loc=1, scale=0.5)

# 1. Регистрация студентов
registration_data = []
for course in courses:
    for student in students[course]:
        registration_data.append({
            'код_курс': course,
            'код_сотрудник': student,
            'дата_регистрация': start_date,
            'дата_отчисление': random_date(start_date + pd.DateOffset(days=30), pd.to_datetime('2023-12-31'))
        })
registration_df = pd.DataFrame(registration_data)

# Добавление сезонных эффектов
registration_df['seasonal_effect'] = registration_df['дата_отчисление'].apply(add_seasonal_effects)
registration_df['дата_отчисление'] = pd.to_datetime(registration_df['дата_отчисление']) + pd.to_timedelta(registration_df['seasonal_effect'], unit='D')
registration_df['дата_отчисление'] = registration_df['дата_отчисление'].dt.floor('D')
registration_df = registration_df.drop(columns='seasonal_effect')

registration_df.to_csv('data/registration.csv', index=False)

# 2. Информация о студентах
students_info_data = []
for course in courses:
    dropouts = random.sample(students[course], random.randint(int(0.05*num_students_per_course), int(0.15*num_students_per_course)))
    for student in students[course]:
        department = random.choice(list(departments.keys()))
        position = random.choice(departments[department])
        status = 'не закончил' if student in dropouts else 'прошел курс'
        students_info_data.append({
            'код_сотрудник': student,
            'код_курс': course,
            'должность': position,
            'отдел': department,
            'пол': random.choice(['жен', 'муж']),
            'возраст': random.randint(20, 60),
            'опыт_работы': random.randint(1, 30),
            'оценка_итог': None,  # Рассчитаем позже
            'статус': status
        })
students_info_df = pd.DataFrame(students_info_data)
students_info_df.to_csv('data/students_info.csv', index=False)

# 3. Задания
assignments_data = []
for course in courses:
    for module in modules[course]:
        assignments_data.append({
            'код_модуль': module,
            'код_курс': course,
            'код_задание': f"экзамен_{module}",
            'тип_задание': 'экзамен по модулю'
        })
        if module == modules[course][-1]:  # Итоговый экзамен только в последнем модуле
            assignments_data.append({
                'код_модуль': module,
                'код_курс': course,
                'код_задание': 'итоговый_экзамен',
                'тип_задание': 'итоговый экзамен'
            })
        for i in range(1, 21):  # 20 тестов на модуль
            assignments_data.append({
                'код_модуль': module,
                'код_курс': course,
                'код_задание': f"тест_{module}_{i}",
                'тип_задание': 'тестирование'
            })
assignments_df = pd.DataFrame(assignments_data)
assignments_df.to_csv('data/assignments.csv', index=False)

# 4. Курсы
courses_data = []
for course in courses:
    for module in modules[course]:
        courses_data.append({
            'код_курс': course,
            'код_модуль': module
        })
courses_df = pd.DataFrame(courses_data)
courses_df.to_csv('data/courses.csv', index=False)

# 5. Материалы
materials_data = []
for course in courses:
    for module in modules[course]:
        for i in range(1, 6):  # 5 материалов на модуль
            materials_data.append({
                'код_материал': f"материал_{i}",
                'код_модуль': module,
                'код_курс': course,
                'тип_материал': random.choice(['видео', 'лекция', 'вебинар', 'тренажер', 'внешний ресурс'])
            })
materials_df = pd.DataFrame(materials_data)
materials_df.to_csv('data/materials.csv', index=False)

# 6. Студенты-Задания
students_assignments_data = []
for course in courses:
    for student in students[course]:
        if students_info_df.loc[students_info_df['код_сотрудник'] == student, 'статус'].values[0] == 'прошел курс':
            for module in modules[course]:
                for i in range(1, 21):  # 20 тестов на модуль
                    date_performed = random_date(start_date + pd.DateOffset(days=30), pd.to_datetime('2023-12-31'))
                    students_assignments_data.append({
                        'код_сотрудник': student,
                        'код_задание': f"тест_{module}_{i}",
                        'дата_выполнения': date_performed,
                        'попытка': random.randint(1, 3),
                        'оценка': random.randint(50, 100)
                    })
                if module == modules[course][-1]:  # Итоговый экзамен только в последнем модуле
                    date_performed = random_date(start_date + pd.DateOffset(days=30), pd.to_datetime('2023-12-31'))
                    students_assignments_data.append({
                        'код_сотрудник': student,
                        'код_задание': 'итоговый_экзамен',
                        'дата_выполнения': date_performed,
                        'попытка': random.randint(1, 3),
                        'оценка': random.randint(50, 100)
                    })
        else:
            num_modules_completed = random.randint(1, num_modules_per_course-1)
            for module in modules[course][:num_modules_completed]:
                for i in range(1, 21):  # 20 тестов на модуль
                    date_performed = random_date(start_date + pd.DateOffset(days=30), pd.to_datetime('2023-12-31'))
                    students_assignments_data.append({
                        'код_сотрудник': student,
                        'код_задание': f"тест_{module}_{i}",
                        'дата_выполнения': date_performed,
                        'попытка': random.randint(1, 3),
                        'оценка': random.randint(50, 100)
                    })
students_assignments_df = pd.DataFrame(students_assignments_data)

# Обновление итоговых оценок студентов
final_grades = students_assignments_df.groupby('код_сотрудник')['оценка'].mean().to_dict()
students_info_df['оценка_итог'] = students_info_df.apply(
    lambda row: final_grades.get(row['код_сотрудник'], None) if row['статус'] == 'прошел курс' else None,
    axis=1
)
students_info_df.to_csv('data/students_info.csv', index=False)
students_assignments_df.to_csv('data/students_assignments.csv', index=False)

# 7. Студенты-Материалы
students_materials_data = []
for course in courses:
    for student in students[course]:
        reg_date = registration_df[(registration_df['код_курс'] == course) & (registration_df['код_сотрудник'] == student)]['дата_регистрация'].values[0]
        end_date = registration_df[(registration_df['код_курс'] == course) & (registration_df['код_сотрудник'] == student)]['дата_отчисление'].values[0]
        for module in modules[course]:
            for i in range(1, 6):  # 5 материалов на модуль
                for _ in range(random.randint(1, 3)):  # материал может быть открыт несколько раз
                    date_accessed = random_date(pd.to_datetime(reg_date), pd.to_datetime(end_date))
                    students_materials_data.append({
                        'код_сотрудник': student,
                        'код_материал': f"материал_{i}",
                        'код_модуль': module,
                        'код_курс': course,
                        'дата': date_accessed,
                        'длительность_пребывания': random.randint(1, 120)  # в минутах
                    })
students_materials_df = pd.DataFrame(students_materials_data)
students_materials_df.to_csv('data/students_materials.csv', index=False)

# 8. Обратная связь
feedback_data = []
for course in courses:
    for student in students[course]:
        for module in modules[course]:
            if random.choice([True, False]):  # Случайным образом добавляем отзывы
                review = random.choice(all_reviews)
                if review in positive_reviews:
                    course_rating = random.randint(4, 5)
                elif review in neutral_reviews:
                    course_rating = 3
                else:
                    course_rating = random.randint(1, 2)
                feedback_data.append({
                    'код_модуль': module,
                    'код_курс': course,
                    'код_сотрудник': student,
                    'оценка_курс': course_rating,
                    'отзыв': review
                })
feedback_df = pd.DataFrame(feedback_data)
feedback_df.to_csv('data/feedback.csv', index=False)





