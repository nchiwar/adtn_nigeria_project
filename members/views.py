# members/views.py (original with correction appended)
from urllib.parse import urlencode
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from .models import MembershipApplication, Publication, ContactMessage, FAQ, News, Event, Job, Member
import logging
from django.utils import timezone
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from .models import Publication
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import default_storage



# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Membership Form
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

# Views
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
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def history(request):
    return render(request, 'core/history.html')

def formation_adtn(request):
    return render(request, 'core/formation_adtn.html')

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

def publications_list(request):
    publications = Publication.objects.all().order_by('-uploaded_at')
    featured_publications = publications[:2]
    recent_publications = publications[2:]
    print(f"Featured Publications: {list(featured_publications)}")
    print(f"Recent Publications: {list(recent_publications)}")
    return render(request, 'core/publications.html', {
        'featured_publications': featured_publications,
        'recent_publications': recent_publications,
    })

def purchase_publication(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    if request.method == 'POST':
        logger.debug(f"Purchase attempted for {publication.title}")
        return render(request, 'core/purchase_confirmation.html', {'publication': publication})
    return render(request, 'core/purchase.html', {'publication': publication})

def news_and_jobs(request):
    news_items = News.objects.all().order_by('-date')  # All news items, newest first
    job_items = Job.objects.all().order_by('-date_posted')  # All job items, newest first
    print(f"News Items: {list(news_items)}")  # Debug output
    print(f"Job Items: {list(job_items)}")    # Debug output
    return render(request, 'core/news.html', {
        'news_items': news_items,
        'job_items': job_items,
        'show_jobs_only': request.path == '/news-and-jobs/'  # Flag to show only jobs
    })

def news_list(request):
    news_items = News.objects.all().order_by('-date')
    return render(request, 'core/news.html', {'news_items': news_items})

def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    return render(request, 'core/news_detail.html', {'news': news})

def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    return render(request, 'core/news_detail.html', {'news': news})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'core/event_detail.html', {'event': event})

def job_detail(request, job_title):
    print(f"View called with job_title: {job_title}")  # Debug output
    try:
        job = Job.objects.get(title=job_title)
        print(f"Job found: {job}")  # Debug output
        return render(request, 'core/job_detail.html', {'job': job})
    except Job.DoesNotExist:
        print(f"Job not found for title: {job_title}")  # Debug output
        raise Http404("Job does not exist")

def submit_job_advert(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        Job.objects.create(title=title, description=description)
        return redirect('news_and_jobs')  # Redirect to news and jobs page
    return render(request, 'core/submit_job_advert.html')

def members_list(request):
    # Try to get members from the database
    members = Member.objects.all()
    # If no members exist, use dummy data
    if not members.exists():
        dummy_members = [
            {'name': 'John Doe'},
            {'name': 'Jane Smith'},
            {'name': 'Ahmed Bello'},
            {'name': 'Chika Okonkwo'},
        ]
        return render(request, 'core/members_list.html', {'members': dummy_members})
    return render(request, 'core/members_list.html', {'members': members})



@login_required
def download_publication(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    if publication.price > 0:
        return redirect(f'/payment/?type=publication&name={publication.title|urlencode}&amount={publication.price}')
    else:
        file_path = publication.file.name  # S3 key (e.g., 'publications/THE_LECRON_Final_with_ISSN_2.pdf')
        file = default_storage.open(file_path, 'rb')
        response = FileResponse(file, as_attachment=True, filename=publication.file.name)
        return response

def publication_list(request):
    featured_publications = Publication.objects.filter(price__gt=0).order_by('-uploaded_at')[:4]
    recent_publications = Publication.objects.filter(price__gte=0).order_by('-uploaded_at')[4:10]
    return render(request, 'publication.html', {
        'featured_publications': featured_publications,
        'recent_publications': recent_publications,
    })

# Correction: Added 'show_jobs_only' flag to news_and_jobs view to control template rendering.