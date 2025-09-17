# members/urls.py (original with correction appended)
from django.urls import path
from . import views

urlpatterns = [
    path('purchase/<int:publication_id>/', views.purchase_publication, name='purchase_publication'),
    path('publications/', views.publications_list, name='publications'),
    path('news/', views.news_list, name='news'),
    path('news-and-jobs/', views.news_and_jobs, name='news_and_jobs'), 
    path('jobs/', views.jobs_view, name='jobs'), # Added named URL
    path('news/<str:job_title>/', views.job_detail, name='job_detail'),
    path('membership/', views.membership_page, name='membership_page'),
    path('members/', views.members_list, name='members_list'),
    path('publications/', views.publication_list, name='publication_list'),
    path('download/<int:pk>/', views.download_publication, name='download_publication'),
]