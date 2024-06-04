import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import plot_tree

# Загрузка данных
def load_data(file_path):
    return pd.read_csv(file_path)

# Подготовка данных для обучения
def prepare_data(data):
    X = data.drop(columns=['статус'])
    y = data['статус'].apply(lambda x: 1 if x == 'прошел курс' else 0)
    return X, y

# Обучение модели с корректировкой гиперпараметров
def train_model(X, y):
    model = RandomForestClassifier(random_state=42)
    
    # Настройки для GridSearchCV
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_features': ['auto', 'sqrt', 'log2'],
        'max_depth': [4, 6, 8],
        'criterion': ['gini', 'entropy']
    }
    
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X, y)
    
    best_model = grid_search.best_estimator_
    return best_model

# Оценка модели
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
    
    # Матрица ошибок
    conf_matrix = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
    plt.title('Матрица ошибок')
    plt.xlabel('Предсказанные значения')
    plt.ylabel('Истинные значения')
    plt.show()

    return y_pred

# Важность признаков
def feature_importance(model, X):
    importances = model.feature_importances_
    feature_names = X.columns
    feature_importance_df = pd.DataFrame({'Признак': feature_names, 'Важность': importances})
    feature_importance_df = feature_importance_df.sort_values(by='Важность', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Важность', y='Признак', data=feature_importance_df)
    plt.title('Важность признаков')
    plt.show()

    return feature_importance_df

# Визуализация дерева решений
def visualize_decision_tree(model, X):
    plt.figure(figsize=(20, 10))
    plot_tree(model.estimators_[0], feature_names=X.columns, filled=True, rounded=True, class_names=['не закончил', 'прошел курс'])
    plt.show()

if __name__ == "__main__":
    # Загрузка данных
    data = load_data('data/processed_students_info.csv')
    
    # Подготовка данных
    X, y = prepare_data(data)
    
    # Разделение данных на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Обучение модели
    model = train_model(X_train, y_train)
    
    # Оценка модели
    y_pred = evaluate_model(model, X_test, y_test)
    
    # Важность признаков
    feature_importance_df = feature_importance(model, X_train)
    
    # Визуализация дерева решений
    visualize_decision_tree(model, X_train)
