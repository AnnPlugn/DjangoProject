import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymysql
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense
def load_and_prepare_data_mysql():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='django_mysql_db'
    )

    query = "SELECT * FROM train_db"
    df = pd.read_sql(query, conn)

    return df

def train_xgboost():
    data = load_and_prepare_data_mysql()
    X = data[['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF']]
    y = data['SalePrice']

    # Нормализация данных
    scaler = MinMaxScaler()
    X_normalized = scaler.fit_transform(X)

    # Разделение данных на обучающий и тестовый наборы
    X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.2, random_state=42)

    # Изменяем форму входных данных
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))

    # Создаем модель SimpleRNN
    model = Sequential()
    model.add(SimpleRNN(32, input_shape=(4, 1)))  # SimpleRNN с 32 нейронами
    model.add(Dense(1, activation='sigmoid'))  # Выходной слой с сигмоидной активацией

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Обучаем модель
    history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

    # Визуализация результатов обучения
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='train_accuracy')
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.savefig('C:/Users/aplyg/PycharmProjects/djangoProjectFirst/static/pik1.png')

    result = {
        'status': 'success',
        'message': 'Модель успешно загружена и визуализирована с помощью гистограмм и диаграммы рассеяния с красными точками'
    }
    return result

