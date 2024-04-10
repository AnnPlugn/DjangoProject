import os
import time
import numpy as np
import pandas as pd
import pymysql
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt

def load_and_prepare_data_mysql(time_step=100):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='django_mysql_db'
    )

    query = "SELECT longitude, latitude, housing_median_age, total_rooms, total_bedrooms, population, households, median_income, median_house_value FROM firstblog_housingdata"
    df = pd.read_sql(query, conn)
    df = pd.DataFrame(df)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_features = scaler.fit_transform(df[['total_bedrooms', 'households', 'population', 'median_income']].values)

    X, Y = [], []
    for i in range(len(scaled_features) - time_step - 1):
        a = scaled_features[i:(i + time_step), :]
        X.append(a)
        Y.append(scaled_features[i + time_step, 0])
    return np.array(X), np.array(Y)

def predict_sql(model, X_test):
    predictions = model.predict(X_test)
    return predictions

def plot_results(predictions, y_test):
    plt.figure(figsize=(12, 6))
    plt.plot(y_test, label='Actual')
    plt.plot(predictions, label='Predicted')
    plt.title('Actual vs Predicted')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.legend()
    plt.savefig('C:/Users/aplyg/PycharmProjects/djangoProjectFirst/static/gradient.png')
    return 'C:/Users/aplyg/PycharmProjects/djangoProjectFirst/static/gradient.png'

def train_sql():
    file_path = "C:/Users/aplyg/PycharmProjects/djangoProjectFirst/firstblog/weights.keras"

    if os.path.exists(file_path):
        result = {
            'status': 'success',
            'message': 'Модель существует'
        }
        visualize_sql()
        return result
    else:
        print(f"Файл {file_path} не существует.")
        time_step = 100
        X, y = load_and_prepare_data_mysql(time_step)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = Sequential()
        model.add(LSTM(50, input_shape=(X_train.shape[1], X_train.shape[2])))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')

        filepath = "weights.keras"
        checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
        callbacks_list = [checkpoint]

        model.fit(X_train, y_train, epochs=50, batch_size=64, validation_data=(X_test, y_test),
                  callbacks=callbacks_list)
        result = {
            'status': 'success',
            'message': 'Модель успешно обучена'
        }
        visualize_sql()
        return result

def visualize_sql():
    time_step = 100
    X, y = load_and_prepare_data_mysql(time_step)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Sequential()
    model.add(LSTM(50, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(1))

    # Загрузка весов модели
    model.load_weights("weights.keras")

    predictions = predict_sql(model, X_test)

    plot_results(predictions, y_test)

