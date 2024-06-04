import pandas as pd
import os
from sklearn.preprocessing import StandardScaler

def load_data(file_path):
    return pd.read_csv(file_path)

def clean_data(data):
    numerical_cols = data.select_dtypes(include=['number']).columns
    if not numerical_cols.empty:
        data[numerical_cols] = data[numerical_cols].fillna(data[numerical_cols].median())
    data = data.drop_duplicates()
    return data

def encode_categorical(data):
    categorical_cols = data.select_dtypes(include=['object']).columns
    if not categorical_cols.empty:
        data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)
    return data

def scale_features(data):
    scaler = StandardScaler()
    numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
    if not numeric_cols.empty:
        data[numeric_cols] = scaler.fit_transform(data[numeric_cols])
    return data

def preprocess_data(file_path):
    data = load_data(file_path)
    data = clean_data(data)
    
    return data

if __name__ == "__main__":
    # Директория для сохранения обработанных данных
    output_dir = '../data/processed/'
    os.makedirs(output_dir, exist_ok=True)

    # Предобработка данных регистрации
    registration_data = preprocess_data('../data/registration.csv')
    registration_data.to_csv(os.path.join(output_dir, 'processed_registration.csv'), index=False)

    # Предобработка данных о студентах
    students_info_data = preprocess_data('../data/students_info.csv')
    students_info_data.to_csv(os.path.join(output_dir, 'processed_students_info.csv'), index=False)

    # Предобработка данных о заданиях
    assignments_data = preprocess_data('../data/assignments.csv')
    assignments_data.to_csv(os.path.join(output_dir, 'processed_assignments.csv'), index=False)

    # Предобработка данных о курсах
    courses_data = preprocess_data('../data/courses.csv')
    courses_data.to_csv(os.path.join(output_dir, 'processed_courses.csv'), index=False)

    # Предобработка данных о материалах
    materials_data = preprocess_data('../data/materials.csv')
    materials_data.to_csv(os.path.join(output_dir, 'processed_materials.csv'), index=False)

    # Предобработка данных студентов-заданий
    students_assignments_data = preprocess_data('../data/students_assignments.csv')
    students_assignments_data.to_csv(os.path.join(output_dir, 'processed_students_assignments.csv'), index=False)

    # Предобработка данных студентов-материалов
    students_materials_data = preprocess_data('../data/students_materials.csv')
    students_materials_data.to_csv(os.path.join(output_dir, 'processed_students_materials.csv'), index=False)

    # Предобработка данных обратной связи
    feedback_data = preprocess_data('../data/feedback.csv')
    feedback_data.to_csv(os.path.join(output_dir, 'processed_feedback.csv'), index=False)

