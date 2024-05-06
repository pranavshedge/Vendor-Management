from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from datetime import timedelta
from purchase_order_tracking.models import PurchaseOrder
from vendor_profile.models import HistoricalPerformance


@receiver(post_save, sender=PurchaseOrder)
@receiver(pre_delete, sender=PurchaseOrder)
def calculate_and_save_on_time_delivery_rate(sender, instance, created, **kwargs):


    if instance.status.lower() == 'completed':
        vendor = instance.vendor
        delivery_date = instance.delivery_date

        # Check if there is an existing record for this vendor and delivery date
        historical_performance, created = HistoricalPerformance.objects.get_or_create(
            vendor=vendor,
        )

        # Count completed POs delivered on or before delivery_date
        completed_orders = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='completed',
            delivery_date__lte=delivery_date
        ).count()


        # Count total completed POs for that vendor
        total_completed_orders = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='completed'
        ).count()


        # Calculate On-Time Delivery Rate
        if total_completed_orders > 0:
            on_time_delivery_rate = (completed_orders / total_completed_orders) * 100
        else:
            on_time_delivery_rate = 0  # To avoid division by zero error

        # Update the on_delivery_rate in HistoricalPerformance
        historical_performance.on_time_delivery_rate = on_time_delivery_rate
        historical_performance.save()


@receiver(post_save, sender=PurchaseOrder)
@receiver(pre_delete, sender=PurchaseOrder)
def update_quality_rating_avg(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor

        # Calculate the average quality rating for completed POs of the vendor
        completed_orders = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='completed',
            quality_rating__isnull=False  # Only consider completed POs with quality ratings
        )
        
        # Calculate the average quality rating
        total_quality_rating = sum(order.quality_rating for order in completed_orders)
        total_completed_orders = completed_orders.count()
        
        if total_completed_orders > 0:
            quality_rating_avg = total_quality_rating / total_completed_orders
        else:
            quality_rating_avg = None  # No completed orders with quality ratings

        # # Update or create HistoricalPerformance record
        historical_performance, created = HistoricalPerformance.objects.get_or_create(
            vendor=vendor,
        )

        historical_performance.quality_rating_avg = quality_rating_avg
        historical_performance.save()


@receiver(post_save, sender=PurchaseOrder)
@receiver(pre_delete, sender=PurchaseOrder)
def update_avg_resp_time(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor

        # Calculate the average response time for acknowledged POs of the vendor
        acknowledged_orders = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='completed',
            acknowledgment_date__isnull=False  # Only consider completed POs with acknowledgment dates
        )
        
        # Calculate the total response time for all acknowledged orders
        total_response_time = timedelta()
        total_acknowledged_orders = 0
        for order in acknowledged_orders:
            if order.acknowledgment_date and order.issue_date:
                total_response_time += order.acknowledgment_date - order.issue_date
                total_acknowledged_orders += 1
        
        # Calculate the average response time
        if total_acknowledged_orders > 0:
            average_response_time = total_response_time / total_acknowledged_orders
        else:
            average_response_time = None  # No acknowledged orders with response times

        # Update or create HistoricalPerformance record
        historical_performance, created = HistoricalPerformance.objects.get_or_create(
            vendor=vendor,
            date=instance.delivery_date,
        )
        historical_performance.average_response_time = average_response_time
        historical_performance.save()


@receiver([post_save, pre_delete], sender=PurchaseOrder)
def update_fullfillment_rate(sender, instance, **kwargs):
    vendor = instance.vendor

    # Calculate the number of successfully fulfilled POs (status 'completed' without issues)
    successful_orders = PurchaseOrder.objects.filter(
        vendor=vendor,
        status='completed',
        quality_rating__isnull=True,  # Exclude orders with quality issues
        issue_date__isnull=False,  # Exclude orders without issue dates
    )

    total_fulfilled_orders = successful_orders.count()

    # Calculate the total number of POs issued to the vendor
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()

    # Calculate the fulfillment rate
    if total_orders > 0:
        fulfillment_rate = (total_fulfilled_orders / total_orders) * 100
    else:
        fulfillment_rate = None  # No POs issued to the vendor

    # Update or create HistoricalPerformance record
    historical_performance, created = HistoricalPerformance.objects.get_or_create(
        vendor=vendor,
        date=instance.delivery_date,
    )
    historical_performance.fulfillment_rate = fulfillment_rate
    historical_performance.save()