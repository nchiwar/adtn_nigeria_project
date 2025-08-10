from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
import logging

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_approved:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('memberspage')
        else:
            messages.error(request, 'Invalid credentials or account not approved.')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def membership_view(request):
    user = request.user
    custom_user = user
    if not custom_user:
        messages.error(request, 'User details not found.')
        return redirect('login')
    context = {
        'email': user.email,
        'full_name': custom_user.full_name,
        'membership_number': custom_user.membership_number,
        'phone': custom_user.phone,
        'address': custom_user.address,
        'membership_type': custom_user.membership_type,
        'joined_date': custom_user.joined_date.strftime('%B %Y') if custom_user.joined_date else 'N/A',
    }
    return render(request, 'core/memberspage.html', context)

def register_view(request):
    if request.method == 'POST':
        messages.info(request, 'Registration is unavailable at the moment.')
        return redirect('register')
    return render(request, 'core/register.html')

def forgot_password_view(request):
    messages.info(request, 'Forgot Password feature is under development. Please contact support for assistance.')
    return redirect('login')