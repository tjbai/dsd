from django.contrib import admin

from .models import Document, Chat


admin.site.register([Document, Chat])