# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_token, name='generate_token'),  # New endpoint for token generation
]
