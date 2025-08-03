from time import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from .models import MembershipApplication, Publication, ContactMessage, FAQ, News, Event, Job
import logging



logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MembershipForm(forms.ModelForm):
    FULL_NAME_CHOICES = [
        ('', 'Select Membership Type'),
        ('Full Membership', 'Full Membership'),
        ('Newly Qualified Membership', 'Newly Qualified Membership'),
        ('Associate Membership', 'Associate Membership'),
        ('Student Membership', 'Student Membership'),
        ('Overseas Membership', 'Overseas Membership'),
        ('6 Month Trial Membership', '6 Month Trial Membership'),
    ]
    EXPERIENCE_CHOICES = [
        ('', 'Select Years of Experience'),
        ('0-2', '0-2'),
        ('3-5', '3-5'),
        ('6-10', '6-10'),
        ('10+', '10+'),
    ]

    class Meta:
        model = MembershipApplication
        fields = ['full_name', 'email', 'phone', 'address', 'password', 'dental_qualification', 'membership_type', 'years_of_experience']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['membership_type'] = forms.ChoiceField(
            choices=self.FULL_NAME_CHOICES,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Membership Type'
        )
        self.fields['years_of_experience'] = forms.ChoiceField(
            choices=self.EXPERIENCE_CHOICES,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Years of Experience'
        )
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

def join_us(request):
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        if form.is_valid():
            application = form.save()
            logger.debug(f"Application saved: {application}")
            return render(request, 'core/join_us.html', {'message': 'Membership application submitted successfully!', 'form': MembershipForm()})
    else:
        form = MembershipForm()
        logger.debug("Form initialized with fields: %s", list(form.fields.keys()))
    return render(request, 'core/join_us.html', {'form': form})

def membership_page(request):
    return render(request, 'core/membership.html')

def home(request):
    return render(request, 'core/home.html')  # Create a basic home.html template if needed

def news_list(request):
    # Add news model and logic here if needed
    return render(request, 'core/news.html')  # Create a news.html template if needed

def about(request):
    # Add news model and logic here if needed
    return render(request, 'core/about.html')  # Create a news.html template if needed

def history(request):
    # Add news model and logic here if needed
    return render(request, 'core/history.html')  # Create a news.html template if needed

def formation_adtn(request):
    # Add news model and logic here if needed
    return render(request, 'core/formation_adtn.html')  # Create a news.html template if needed

def contact(request):
    # Add news model and logic here if needed
    return render(request, 'core/placeholder.html')  # Create a news.html template if needed

def placeholder(request):
    # Add news model and logic here if needed
    return render(request, 'core/placeholder.html')  # Create a news.html template if needed

def faq(request):
    return render(request, 'core/faq.html')

def publications_page(request):
    featured_publications = Publication.objects.order_by('-uploaded_at')[:2]
    recent_publications = Publication.objects.order_by('-uploaded_at')[2:8]
    return render(request, 'core/publications.html', {
        'featured_publications': featured_publications,
        'recent_publications': recent_publications
    })

def purchase_publication(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    if request.method == 'POST':
        # Here you would integrate a payment gateway (e.g., Stripe, PayPal)
        # For now, simulate a successful purchase
        logger.debug(f"Purchase attempted for {publication.title}")
        return render(request, 'core/purchase_confirmation.html', {'publication': publication})
    return render(request, 'core/purchase.html', {'publication': publication})

def publications_page(request):
    featured_publications = Publication.objects.order_by('-uploaded_at')
    return render(request, 'core/publications.html', {
        'featured_publications': featured_publications,
    })

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        membership_number = request.POST.get('membership_number', '')
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        message = request.POST.get('message', '')
        consent = 'consent' in request.POST

        contact_message = ContactMessage(
            name=name,
            membership_number=membership_number,
            email=email,
            phone=phone,
            address=address,
            message=message,
            consent=consent
        )
        contact_message.save()

        # Send email notification (optional)
        subject = f'New Contact Message from {name}'
        message_body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nAddress: {address}\nMessage: {message}\nConsent: {consent}"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = ['dta@dentalng.org']  # Replace with your admin email
        send_mail(subject, message_body, from_email, to_email, fail_silently=True)

        return redirect('contact_success')

    return render(request, 'core/contact.html')

def contact_success(request):
    return render(request, 'core/contact_success.html')

def faq(request):
    membership_faqs = FAQ.objects.filter(category='membership')
    ecpd_faqs = FAQ.objects.filter(category='ecpd')
    regulation_faqs = FAQ.objects.filter(category='regulation')
    payment_faqs = FAQ.objects.filter(category='payment')
    return render(request, 'core/faq.html', {
        'membership_faqs': membership_faqs,
        'ecpd_faqs': ecpd_faqs,
        'regulation_faqs': regulation_faqs,
        'payment_faqs': payment_faqs,
    })
def news(request):
    news_items = News.objects.all().order_by('-date')[:4]
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    return render(request, 'core/news.html', {'news_items': news_items, 'events': events})

def jobs(request):
    jobs = Job.objects.all().order_by('-date_posted')[:5]
    return render(request, 'core/jobs.html', {'jobs': jobs})

def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    return render(request, 'core/news_detail.html', {'news': news})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'core/event_detail.html', {'event': event})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'core/job_detail.html', {'job': job})

def submit_job_advert(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        Job.objects.create(title=title, description=description)
        return redirect('jobs')
    return render(request, 'core/submit_job_advert.html')