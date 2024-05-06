from django.contrib import admin
from .models import PurchaseOrder  # Import your model from your app's models.py file

# Register your models here
admin.site.register(PurchaseOrder)
