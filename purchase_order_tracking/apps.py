from django.apps import AppConfig


class PurchaseOrderTrackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'purchase_order_tracking'

    def ready(self):
        from django.db.models.signals import post_save, pre_delete
        from purchase_order_tracking.models import PurchaseOrder
        from vendor_profile.models import HistoricalPerformance

        # Connect signal handlers
        from purchase_order_tracking.api import signals
