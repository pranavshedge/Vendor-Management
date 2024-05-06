# views.py
from rest_framework import status
from django.db.models import Avg
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from vendor_profile.models import Vendor
from .serializers import VendorSerializer,HistoricalPerformanceSerializer
from django.shortcuts import get_object_or_404
from purchase_order_tracking.models import PurchaseOrder
from vendor_profile.models import HistoricalPerformance
from datetime import datetime
from authentication.authentication import CustomTokenAuthentication


@api_view(['POST'])
@authentication_classes([CustomTokenAuthentication])
def create_vendor(request):
    serializer = VendorSerializer(data=request.data)


    if serializer.is_valid():
        record = serializer.save()
        vendor_id = record.pk

        historical_performance_data = {
            'vendor': vendor_id,
            'date': datetime.now(),  # Assuming 'date' is a DateTimeField in HistoricalPerformance
            'on_time_delivery_rate': 0,  # Assuming these fields are FloatFields
            'quality_rating_avg': 0,
            'average_response_time': 0,
            'fulfillment_rate': 0
        }

        historical_performance_serializer = HistoricalPerformanceSerializer(data=historical_performance_data)
        
        if historical_performance_serializer.is_valid():
            historical_performance_serializer.save()
            
        return Response({"message": "Vendor created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
def list_vendors(request):
    vendors = Vendor.objects.all()
    serializer = VendorSerializer(vendors, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([CustomTokenAuthentication])
def vendor_detail(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({"message": "Vendor details not found"},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.update(vendor, serializer.validated_data)
            return Response({"message": f"Vendor Details with ID {vendor_id} updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vendor.delete()
        return Response({"message": f"Vendor Details with ID {vendor_id} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
def vendor_performance(request, vendor_id):
    # Retrieve the vendor instance
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    # Retrieve the historical performance data for the vendor
    historical_performance = HistoricalPerformance.objects.filter(vendor=vendor)

    # Calculate average values
    on_time_delivery_rate_avg = historical_performance.aggregate(avg_on_time_delivery_rate=Avg('on_time_delivery_rate'))['avg_on_time_delivery_rate']
    
    quality_rating_avg_avg = historical_performance.aggregate(avg_quality_rating_avg=Avg('quality_rating_avg'))['avg_quality_rating_avg']
    
    average_response_time_avg = historical_performance.aggregate(avg_average_response_time=Avg('average_response_time'))['avg_average_response_time']
    
    fulfillment_rate_avg = historical_performance.aggregate(avg_fulfillment_rate=Avg('fulfillment_rate'))['avg_fulfillment_rate']

    # Prepare response data
    performance_data = {
        'on_time_delivery_rate': on_time_delivery_rate_avg,
        'quality_rating_avg': quality_rating_avg_avg,
        'average_response_time': average_response_time_avg,
        'fulfillment_rate': fulfillment_rate_avg,
    }

    return Response(performance_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([CustomTokenAuthentication])
def acknowledge_purchase_order(request, po_id):
    try:
        # Retrieve the purchase order instance
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
        
        # Update acknowledgment_date
        purchase_order.acknowledgment_date = datetime.now()
        purchase_order.save()

        return Response({"message": "Purchase Order acknowledged successfully"}, status=status.HTTP_200_OK)
    except PurchaseOrder.DoesNotExist:
        return Response({"message": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)