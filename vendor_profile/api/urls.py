# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_vendor),
    path('', views.list_vendors),
    path('<int:vendor_id>', views.vendor_detail),
    path('vendors/<int:vendor_id>/performance/', views.vendor_performance, name='vendor_performance')
]
