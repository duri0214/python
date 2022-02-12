from django.contrib import admin

# Register your models here.
from .models import Staff, Store, Schedule
admin.site.register([Staff, Store, Schedule])
