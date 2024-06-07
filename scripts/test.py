import pandas as pd
import numpy as np

# Генерация тестовых данных
np.random.seed(0)

# Данные студентов
students_info = pd.DataFrame({
    'код_сотрудник': np.arange(1, 101),
    'код_курс': np.random.choice(['курс_1', 'курс_2'], 100),
    'оценка_итог': np.random.randint(50, 100, 100)
})

# Данные заданий
assignments = pd.DataFrame({
    'код_сотрудник': np.random.choice(students_info['код_сотрудник'], 300),
    'код_задание': np.random.randint(1, 10, 300),
    'оценка': np.random.randint(0, 100, 300),
    'попытка': np.random.randint(1, 4, 300)
})

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

# Вызов функции
cognitive_load = cognitive_load_assessment(assignments, students_info)

# Вывод результата
print("Оценка когнитивной посильности:")
print(cognitive_load)
