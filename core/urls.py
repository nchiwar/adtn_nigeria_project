# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.news_list, name='news'),
    path('history/', views.history, name='history'),
    path('formation-adtn/', views.formation_adtn, name='formation_adtn'),
    path('placeholder/', views.placeholder, name='placeholder'),
    
]