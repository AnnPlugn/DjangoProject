import pandas as pd
from django.http import JsonResponse
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
import os
import pymysql
from sklearn.model_selection import train_test_split

def load_and_prepare_data_mysql():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='django_mysql_db'
    )

    query = "SELECT longitude, latitude, housing_median_age, total_rooms, total_bedrooms, population, households, median_income, median_house_value FROM firstblog_housingdata"
    df = pd.read_sql(query, conn)

    features = df[['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income']].values
    target = df['median_house_value'].values

    scaler = MinMaxScaler(feature_range=(0, 1))
    features_scaled = scaler.fit_transform(features)

    conn.close()

    return features_scaled, target

def train_xgboost():
    X, y = load_and_prepare_data_mysql()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.08, gamma=0, subsample=0.75, colsample_bytree=1,
                             max_depth=7)
    model.fit(X_train, y_train)

    model_dir = 'mymodel_mysql'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    model.save_model(f'{model_dir}/my_xgb_model.json')

    result = {
        'status': 'success',
        'message': 'Модель успешно обучена'
    }
    return result

train_xgboost()