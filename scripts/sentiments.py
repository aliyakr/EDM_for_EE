import pandas as pd
from transformers import pipeline

# Функция для загрузки данных
def load_data(file_path):
    return pd.read_csv(file_path)

# Функция для анализа тональности
def sentiment_analysis(text, model):
    result = model(text)
    return result[0]['label'], result[0]['score']

if __name__ == "__main__":
    # Загрузка данных обратной связи
    feedback_data = load_data('data/feedback.csv')
    
    # Инициализация модели для анализа тональности
    sentiment_model = pipeline('sentiment-analysis', model='blanchefort/rubert-base-cased-sentiment')
    
    # Применение анализа тональности к каждому отзыву
    feedback_data['тональность'], feedback_data['оценка_тональности'] = zip(*feedback_data['отзыв'].apply(lambda x: sentiment_analysis(x, sentiment_model)))
    
    # Сохранение результатов анализа тональности
    feedback_data.to_csv('data/feedback_with_sentiment.csv', index=False)

    print("Анализ тональности завершен. Результаты сохранены в 'data/feedback_with_sentiment.csv'.")
