import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Generate mock data
def generate_mock_data(n_samples=100):
    np.random.seed(42)
    data = pd.DataFrame({
        'оценка_пользователя': np.random.rand(n_samples),
        'оценка_тональности': np.random.rand(n_samples),
        'время_на_материале': np.random.rand(n_samples),
        'процент_завершения_заданий': np.random.rand(n_samples),
        'процент_успешных_заданий': np.random.rand(n_samples),
        'когнитивная_посильность': np.random.rand(n_samples),
        'показатель_качества': np.random.rand(n_samples)
    })
    return data

# Подготовка данных для обучения
def prepare_data(data):
    X = data.drop(columns=['показатель_качества'])
    y = data['показатель_качества']
    return X, y

# Обучение модели с корректировкой гиперпараметров
def train_model(X, y):
    model = LinearRegression()
    
    # Настройки для GridSearchCV
    param_grid = {
        'fit_intercept': [True, False]
    }
    
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='r2', n_jobs=-1)
    grid_search.fit(X, y)
    
    best_model = grid_search.best_estimator_
    return best_model

# Оценка модели
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f'Mean Squared Error: {mse}')
    print(f'Mean Absolute Error: {mae}')
    print(f'R^2 Score: {r2}')
    
    return y_pred

# Прогнозирование
def predict(model, X):
    return model.predict(X)

# Интерпретация результатов
def interpret_results(y_test, y_pred):
    residuals = y_test - y_pred
    
    # Анализ остатков
    plt.figure(figsize=(10, 6))
    sns.histplot(residuals, kde=True)
    plt.title('Распределение остатков')
    plt.xlabel('Остатки')
    plt.ylabel('Частота')
    plt.show()
    
    # Визуализация ошибок
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, residuals)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.title('График остатков')
    plt.xlabel('Фактические значения')
    plt.ylabel('Остатки')
    plt.show()

if __name__ == "__main__":
    # Generate mock data
    data = generate_mock_data(100)
    
    # Подготовка данных
    X, y = prepare_data(data)
    
    # Разделение данных на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Обучение модели
    model = train_model(X_train, y_train)
    
    # Оценка модели
    y_pred = evaluate_model(model, X_test, y_test)
    
    # Прогнозирование
    predictions = predict(model, X_test)
    
    # Интерпретация результатов
    interpret_results(y_test, y_pred)
