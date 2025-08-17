from django.contrib import admin
from .models import CustomUser, Official

admin.site.register(CustomUser)
admin.site.register(Official)