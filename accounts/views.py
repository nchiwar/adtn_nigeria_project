from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser  # Only import CustomUser from accounts.models
from core.models import About, Official  # Import About and Official from core.models
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
        email = request.POST['email']
        username = request.POST['username']
        full_name = request.POST['full_name']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        # Check if passwords match
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # Check if email or username already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')

        # Create new user with membership_type (e.g., default to 'Basic' or from POST)
        membership_type = request.POST.get('membership_type', 'Basic')  # Add membership_type to form
        new_user = CustomUser.objects.create_user(
            username=username,
            email=email,
            full_name=full_name,
            membership_type=membership_type,
            password=password
        )
        new_user.is_approved = False  # Require admin approval
        new_user.save()

        messages.success(request, 'Registration successful! Awaiting admin approval.')
        return redirect('login')
    return render(request, 'core/register.html')

def forgot_password_view(request):
    messages.info(request, 'Forgot Password feature is under development. Please contact support for assistance.')
    return redirect('login')

def about_view(request):
    about_data = About.objects.first()  # Fetch the first About record
    officials = Official.objects.all()  # Fetch all officials
    logger.debug(f"About.objects.all(): {list(About.objects.all())}")  # Log all About records
    if about_data:
        logger.debug(f"About data retrieved: {about_data.__dict__}")
    else:
        logger.warning("No About data found in the database.")
    context = {
        'about_description': about_data.about_description if about_data else "No description available",
        'mission': about_data.mission if about_data else "No mission available",
        'vision': about_data.vision if about_data else "No vision available",
        'core_values': about_data.core_values if about_data else "No core values available",
        'goals': about_data.goals if about_data else "No goals available",
        'history_summary': about_data.history_summary if about_data else "No history available",
        'formation_summary': about_data.formation_summary if about_data else "No formation details available",
        'officials': officials,
    }
    if about_data and about_data.goals:
        context['goals_list'] = [goal.strip() for goal in about_data.goals.replace('\\n', '\n').split('\n') if goal.strip()]
        logger.debug(f"goals_list: {context['goals_list']}")
    else:
        context['goals_list'] = ["No goals available"]
    logger.debug(f"Context: {context}")  # Log the final context
    return render(request, 'core/about.html', context)

# Additional helper to restrict members page to approved users with membership
@login_required
def memberspage_view(request):
    user = request.user
    if not user.is_approved or not user.membership_type:
        messages.error(request, 'You need an approved membership to access this page.')
        return redirect('login')
    return membership_view(request)  # Reuse membership_view logic