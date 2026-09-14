from django.shortcuts import get_object_or_404 
from rest_framework.decorators import api_view , permission_classes
from .models import Order, OrderItem 
from product.models import Product
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from rest_framework import status
# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    order = Order.objects.all()
    serializers =OrderSerialilzers(order,many = True)
    return Response({'orders':serializers.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request,pk):
    order = get_object_or_404(Order , id = pk)
    serializers =OrderSerialilzers(order,many = False)
    return Response({'orders':serializers.data})


@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def update_status_order(request,pk):
    order = get_object_or_404(Order , id = pk)
    order.status = request.data['status']
    order.save()
    serializers =OrderSerialilzers(order,many = False)
    return Response({'orders':serializers.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request,pk):
    order = get_object_or_404(Order , id = pk)
    order.delete()
    
    return Response({'details':"order is deleted successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
    user =request.user
    incoming_data = request.data 
    order_items = incoming_data.get('order_items')

    if not order_items and len(order_items) == 0:
        return Response ({"error":"No Order Recieved"},status=status.HTTP_400_BAD_REQUEST)
    else:
        total_amount = sum(item['price'] * item['quantity'] for item in order_items)
        order = Order.objects.create(
            user =user,
            city =  incoming_data.get('city'),
            zipcode = incoming_data.get('zipcode'),
            street = incoming_data.get('street'),
            phone_no = incoming_data.get('phone_no'),
            country = incoming_data.get('country'),
            total_amount = total_amount 
        )
        for i in order_items:
            product = Product.objects.get(id = i['product'])
            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                quantity = i['quantity'],
                price = i['price']

            )
            product.stock -= item.quantity
            product.save()
        serializers = OrderSerialilzers(order,many = False)
        return Response(serializers.data)
  