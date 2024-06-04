import pandas as pd
import numpy as np

# Загрузка данных
def load_data(file_path):
    return pd.read_csv(file_path)

# Нормализация данных
def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

# Расчет показателя качества
def calculate_quality_score(feedback_data, materials_data, assignments_data, weights):
    # Прямая оценка пользователя
    user_ratings = normalize(feedback_data.groupby('код_материал')['оценка_курс'].mean())

    # Вероятностный показатель тональности (от -1 до 1)
    sentiment_scores = normalize(feedback_data.groupby('код_материал')['оценка_тональности'].mean() * 2 - 1)

    # Время, проведенное на материале (в минутах)
    time_spent = normalize(materials_data.groupby('код_материал')['длительность_пребывания'].mean())

    # Процент завершенных заданий
    completed_assignments = assignments_data.groupby('код_сотрудник')['код_задание'].nunique()
    total_assignments = assignments_data['код_задание'].nunique()
    assignment_completion_rate = normalize(completed_assignments / total_assignments)

    # Процент успешного выполнения заданий
    successful_assignments = assignments_data[assignments_data['оценка'] >= 70].groupby('код_сотрудник')['код_задание'].nunique()
    assignment_success_rate = normalize(successful_assignments / total_assignments)

    # Слияние всех показателей в один DataFrame
    quality_df = pd.DataFrame({
        'оценка_пользователя': user_ratings,
        'оценка_тональности': sentiment_scores,
        'время_на_материале': time_spent,
        'процент_завершения_заданий': assignment_completion_rate,
        'процент_успешных_заданий': assignment_success_rate
    }).fillna(0)

    # Расчет итогового показателя качества
    quality_df['показатель_качества'] = (weights['оценка_пользователя'] * quality_df['оценка_пользователя'] +
                                         weights['оценка_тональности'] * quality_df['оценка_тональности'] +
                                         weights['время_на_материале'] * quality_df['время_на_материале'] +
                                         weights['процент_завершения_заданий'] * quality_df['процент_завершения_заданий'] +
                                         weights['процент_успешных_заданий'] * quality_df['процент_успешных_заданий'])
    
    return quality_df

if __name__ == "__main__":
    # Загрузка данных
    feedback_data = load_data('data/feedback_with_sentiment.csv')
    materials_data = load_data('data/processed_students_materials.csv')
    assignments_data = load_data('data/processed_students_assignments.csv')

    # Весовые коэффициенты
    weights = {
        'оценка_пользователя': 0.3,
        'оценка_тональности': 0.2,
        'время_на_материале': 0.2,
        'процент_завершения_заданий': 0.2,
        'процент_успешных_заданий': 0.1
    }

    # Расчет показателя качества
    quality_scores = calculate_quality_score(feedback_data, materials_data, assignments_data, weights)

    # Сохранение результатов
    quality_scores.to_csv('data/quality_scores.csv', index=False)

    print("Расчет показателя качества завершен. Результаты сохранены в 'data/quality_scores.csv'.")
