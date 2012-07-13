from django.contrib import admin
from .models import Company, Location, Job

admin.site.register(Company)
admin.site.register(Location)
admin.site.register(Job)