from django.contrib import admin
from .models import FAQ, ContactMessage, Publication, News, Event, Job, Member

admin.site.register(FAQ)
admin.site.register(ContactMessage)
admin.site.register(Publication)
admin.site.register(News)
admin.site.register(Event)
admin.site.register(Job)
admin.site.register(Member)