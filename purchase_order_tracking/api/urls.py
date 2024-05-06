# urls.py
from django.urls import path
from .views import create_and_list_purchase_order,purchase_order_detail

urlpatterns = [
    path('', create_and_list_purchase_order, name='create-and-list-purchase-order'),
    # path('', list_purchase_orders, name='list-purchase-orders'),
    path('<int:po_id>/', purchase_order_detail, name='purchase-order-detail'),
]
