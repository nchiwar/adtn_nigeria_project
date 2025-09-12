from django.urls import path
from . import views
from .models import Purchase


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('memberspage/', views.membership_view, name='memberspage'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('about/', views.about_view, name='about'),
    path('payment/', views.payment_view, name='payment'),
    path('subscription-success/', views.subscription_success, name='subscription_success'),
    path('purchase-success/', views.purchase_success, name='purchase_success'),
]