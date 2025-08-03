from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CustomUser
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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

def login_view(request):
    print(f"CSRF Cookie: {request.COOKIES.get('csrftoken')}")
    if not request.session.session_key:
        request.session.create()
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = CustomUser.objects.filter(email=email).first()  # Direct query
        print(f"Auth attempt for {email}: User={user}, Approved={user.is_approved if user else 'N/A'}, Password check={user.check_password(password) if user else 'N/A'}")
        if user and user.check_password(password) and user.is_approved:
            login(request, user)
            messages.success(request, 'Login successful!')
            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('memberspage')
        else:
            messages.error(request, 'Invalid credentials or account not approved.')
    return render(request, 'core/login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        full_name = request.POST['full_name']
        membership_number = request.POST['membership_number']
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'core/register.html')
        if CustomUser.objects.filter(membership_number=membership_number).exists():
            messages.error(request, 'Membership number already in use.')
            return render(request, 'core/register.html')
        
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            full_name=full_name,
            membership_number=membership_number,
            is_approved=True,
            is_superuser=False,
            is_staff=False
        )
        print("User created:", user.email, user.is_approved)
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')
    return render(request, 'core/register.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def forgot_password_view(request):
    messages.info(request, 'Forgot password functionality is under development.')
    return render(request, 'core/login.html')