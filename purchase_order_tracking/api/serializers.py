from rest_framework import serializers
from purchase_order_tracking.models import PurchaseOrder

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only_fields = ('po_number',)  # Make po_number read-only
        extra_kwargs = {
            'vendor': {'required': False}  # Allow vendor to be optional for partial updates
        }