"""
URL configuration for adtn_nigeria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py (original with correction appended)
from django.contrib import admin
from django.urls import path, include
from core import views
from members.views import membership_page, join_us
from members import views
from django.conf import settings
from django.conf.urls.static import static
from members.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('core.urls')),
    path('', include('members.urls')),
    path('', home_view, name='home'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('formation-adtn/', views.formation_adtn, name='formation_adtn'),
    path('membership/', views.membership_page, name='membership_page'),
    path('join-us/', join_us, name='join_us'),
    path('purchase/<int:publication_id>/', views.purchase_publication, name='purchase_publication'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.contact, name='contact_submit'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('faq/', views.faq, name='faq'),
    # Removed: path('news/Job/', views.Job, name='Job')  # Incorrect reference to Job model
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),  # Adjusted to match members/urls.py intent
    path('submit-job-advert/', views.submit_job_advert, name='submit_job_advert'),   
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
