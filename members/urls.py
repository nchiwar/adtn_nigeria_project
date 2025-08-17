# members/urls.py (original with correction appended)
from django.urls import path
from . import views

urlpatterns = [
    path('purchase/<int:publication_id>/', views.purchase_publication, name='purchase_publication'),
    path('publications/', views.publications_list, name='publications'),
    path('news/', views.news_list, name='news'),
    path('news-and-jobs/', views.news_and_jobs, name='news_and_jobs'),  # Added named URL
    path('news/<str:job_title>/', views.job_detail, name='job_detail'),
]