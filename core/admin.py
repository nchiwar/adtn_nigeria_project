# core/admin.py
from django.contrib import admin
from .models import CpdArticle, About, Official, History, Formation

admin.site.register(CpdArticle)
admin.site.register(About)
admin.site.register(Official)
admin.site.register(History)
admin.site.register(Formation)