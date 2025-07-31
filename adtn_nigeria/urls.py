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

from django.contrib import admin
from django.urls import path, include
from core import views
from members.views import membership_page, join_us
from members import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('news/', views.news_list, name='news'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('formation-adtn/', views.formation_adtn, name='formation_adtn'),
   path('membership/', views.membership_page, name='membership_page'),
    path('join-us/', join_us, name='join_us'),
    path('publications/', views.publications_page, name='publications_page'),
    path('purchase/<int:publication_id>/', views.purchase_publication, name='purchase_publication'),
    path('contact/', views.placeholder, name='contact'),
    path('login/', views.placeholder, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)