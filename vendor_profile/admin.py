from django.contrib import admin
from .models import Vendor,HistoricalPerformance  # Import your model from your app's models.py file

# Register your models here
admin.site.register(Vendor)
admin.site.register(HistoricalPerformance)