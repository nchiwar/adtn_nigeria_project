from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django import forms
from .models import MembershipApplication, Publication
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

 