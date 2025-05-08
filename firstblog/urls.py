from django.urls import path
from . import views

app_name = 'firstblog'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('result/', views.result, name='result'),
    path('invoke_model/', views.invoke_model, name='invoke_model'),
    path('train_polynomial_regression_model/', views.train_polynomial_regression_model, name='train_polynomial_regression_model'),
    path('train_sql/', views.train_sql, name='train_sql'),
    path('train_xgboost/', views.train_xgboost, name='train_xgboost'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]