from .views import PolinomTrainView, AboutPageView, InputPageView, PolinomView, XGBoostTrainView, GradientTrainView
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.post_list, name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('imput/', InputPageView.as_view(), name='imput'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('result/', PolinomView.as_view(), name='result'),
    path('train_polynomial_regression_model/', PolinomTrainView.as_view(), name='train_polynomial_regression_model'),
    path('train_xgboost/', XGBoostTrainView.as_view(), name='train_xgboost'),
    path('train_sql/', GradientTrainView.as_view(), name='train_sql'),
    path('create', views.create, name='create')
]
