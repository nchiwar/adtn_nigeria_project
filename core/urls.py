from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('formation-adtn/', views.formation_adtn, name='formation_adtn'),
    # Add other paths as needed
]