from .views import BlogListView, AboutPageView, InputPageView
from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.post_list, name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('imput/', InputPageView.as_view(), name='imput'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
