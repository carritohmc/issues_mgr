from django.contrib import admin
from .models import Issue, Team


admin.site.register([Issue, Team])
