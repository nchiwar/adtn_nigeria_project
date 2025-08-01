from django.contrib import admin
from .models import FAQ, ContactMessage, Publication

admin.site.register(FAQ)
admin.site.register(ContactMessage)
admin.site.register(Publication)