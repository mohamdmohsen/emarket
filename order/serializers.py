from rest_framework import serializers
from .models import *

class OrderSerializers(serializers.ModelSerializer):


    class Meta :
        model = Order
        fields = "__all__"


class OrderItemSerialilzers(serializers.ModelSerializer):
        orderitems =serializers.SerializerMethodField(method_name="get_order_items",read_only= True)

        class Meta:
            model = OrderItem
            fields = "__all__"