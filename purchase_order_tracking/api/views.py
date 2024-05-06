# views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from authentication.authentication import CustomTokenAuthentication
from purchase_order_tracking.models import PurchaseOrder
from .serializers import PurchaseOrderSerializer


def create_purchase_order(request):
    serializer = PurchaseOrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": f"Purchase order created successfully with ID {serializer.data['id']}"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def list_purchase_orders(request):
    vendor_id = request.query_params.get('vendor', None)
    if vendor_id:
        purchase_orders = PurchaseOrder.objects.filter(vendor=vendor_id)
    else:
        purchase_orders = PurchaseOrder.objects.all()
    serializer = PurchaseOrderSerializer(purchase_orders, many=True)
    return Response(serializer.data)



@api_view(['POST', 'GET'])
@authentication_classes([CustomTokenAuthentication])
def create_and_list_purchase_order(request):
    if request.method == 'GET':
        return list_purchase_orders(request)
    elif request.method == 'POST':
        return create_purchase_order(request)



@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([CustomTokenAuthentication])
def purchase_order_detail(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response({"message": "Purchase order details not found"},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(purchase_order, serializer.validated_data)
            serializer.save()
            return Response({"message": f"Purchase order with Row ID: {po_id} and PO Number: {purchase_order} updated successfully"}, status=status.HTTP_200_OK)
        else:
            print('invalid serializer')
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        purchase_order.delete()
        return Response({"message": f"Purchase order with ID {po_id} deleted successfully"},status=status.HTTP_204_NO_CONTENT)
