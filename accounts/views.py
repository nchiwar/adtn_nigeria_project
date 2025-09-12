from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import CustomUser, Subscription, Purchase  # Import all required models
from core.models import About, Official  # Import About and Official from core.models
import logging
import paystack
from django.conf import settings

logger = logging.getLogger(__name__)

# Set Paystack API key from settings
paystack.api_key = settings.PAYSTACK_SECRET_KEY

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
        'phone': custom_user.phone or 'N/A',
        'address': custom_user.address or 'N/A',
        'membership_type': custom_user.get_membership_type_display(),
        'joined_date': custom_user.joined_date.strftime('%B %Y') if custom_user.joined_date else 'N/A',
        'profile_image': custom_user.profile_image.url if custom_user.profile_image else None,
    }
    return render(request, 'core/memberspage.html', context)

def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        full_name = request.POST['full_name']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        membership_number = request.POST.get('membership_number')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        membership_type = request.POST.get('membership_type', 'full')  # Updated to match choices
        joined_date = request.POST.get('joined_date')
        profile_image = request.FILES.get('profile_image')
        subscribe = request.POST.get('subscribe') == 'true'
        subscription_amount = float(request.POST.get('subscription_amount', 0.00))

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')

        new_user = CustomUser.objects.create_user(
            username=username,
            email=email,
            full_name=full_name,
            membership_number=membership_number,
            phone=phone,
            address=address,
            membership_type=membership_type,
            joined_date=joined_date if joined_date else None,
            password=password
        )
        if profile_image:
            new_user.profile_image = profile_image
        new_user.is_approved = False
        new_user.save()

        if subscribe:
            try:
                response = paystack.Transaction.initialize(
                    email=email,
                    amount=int(subscription_amount * 100),  # In kobo
                    reference=f'reg-sub-{username}-{timezone.now().timestamp()}',
                    callback_url=request.build_absolute_uri('/subscription-success/'),
                    metadata={'custom_fields': [{'display_name': 'Membership Type', 'variable_name': 'membership_type', 'value': membership_type}]}
                )
                return redirect(response['data']['authorization_url'])
            except Exception as e:
                logger.error(f'Paystack initialization failed: {str(e)}')
                messages.error(request, f'Payment setup failed: {str(e)}')
                return redirect('register')

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

@login_required
def memberspage_view(request):
    user = request.user
    if not user.is_approved or not user.membership_type:
        messages.error(request, 'You need an approved membership to access this page.')
        return redirect('login')
    return membership_view(request)  # Reuse membership_view logic

@login_required
def payment_view(request):
    item_type = request.GET.get('type')
    item_name = request.GET.get('name')
    amount = float(request.GET.get('amount', 0.00))
    context = {
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
        'item_type': item_type,
        'item_name': item_name,
        'amount': amount,
    }
    return render(request, 'core/payment.html', context)

def subscription_success(request):
    user = request.user
    trxref = request.GET.get('trxref')
    if trxref:
        try:
            response = paystack.Transaction.verify(trxref)
            if response['data']['status'] == 'success':
                subscription, created = Subscription.objects.get_or_create(user=user)
                subscription.status = 'active'
                subscription.membership_type = user.membership_type
                subscription.end_date = timezone.now() + timezone.timedelta(days=365)
                subscription.save()
                messages.success(request, 'Subscription activated successfully!')
                return render(request, 'core/subscription_success.html')
        except Exception as e:
            logger.error(f'Paystack verification failed: {str(e)}')
            messages.error(request, f'Payment verification failed: {str(e)}')
    return redirect('register')

def purchase_success(request):
    user = request.user
    trxref = request.GET.get('trxref')
    if trxref:
        try:
            response = paystack.Transaction.verify(trxref)
            if response['data']['status'] == 'success':
                item_type = request.GET.get('item_type')
                item_name = request.GET.get('item_name')
                amount = float(request.GET.get('amount', 0.00))
                Purchase.objects.create(user=user, item_type=item_type, item_name=item_name, amount=amount, paystack_reference=trxref)
                messages.success(request, 'Purchase completed successfully!')
                return render(request, 'core/purchase_success.html')
        except Exception as e:
            logger.error(f'Paystack verification failed: {str(e)}')
            messages.error(request, f'Payment verification failed: {str(e)}')
    return redirect('memberspage')