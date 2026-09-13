from django.db import models
from operator import  mod
from django.contrib.auth.models import User
from product.models import Product
# Create your models here.

class OrderStatus(models.TextChoices):
    PROCCESSING ="Proccessing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"


class PaymentStatus(models.TextChoices):
    PAID ="Paid"
    UNPAID = "Unpaid"


class PaymentMod(models.TextChoices):
    CASH_ON_DELIVERED ="Cash on Delivered"
    CARD = "CARD"
        
class Order(models.Model):
    city =models.CharField(max_length=400,default="",blank=False)
    zipcode = models.CharField(max_length=100,default="",blank=False)
    street = models.CharField(max_length=500, default="", blank=False)
    state = models.CharField(max_length=100,default="",blank=False)
    country = models.CharField(max_length=100, default="",blank=False)
    phone_no = models.CharField(max_length=20, default="",blank=False)
    total_amount =models.IntegerField(default=0 )
    Payment_Status =models.CharField(max_length=30,choices=PaymentStatus.choices ,default=PaymentStatus.UNPAID)
    payment_mod = models.CharField(max_length=30 ,choices=PaymentMod ,default=PaymentMod.CARD)
    staus = models.CharField(max_length=60, choices=OrderStatus ,default=OrderStatus.PROCCESSING)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.id)

        
class OrderItem(models.Model):
    product = models.ForeignKey(Product,null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order,null=True, on_delete=models.CASCADE, related_name='orderitems')
    name =models.CharField(max_length=200,default="",blank=False)
    quantity = models.IntegerField(default=1)
    quantity = models.DecimalField(max_digits=7,decimal_places=2 ,blank=False)

    city =models.CharField(max_length=400,default="",blank=False)
    zipcode = models.CharField(max_length=100,default="",blank=False)
    street = models.CharField(max_length=500, default="", blank=False)
    state = models.CharField(max_length=100,default="",blank=False)
    country = models.CharField(max_length=100, default="",blank=False)
    phone_no = models.CharField(max_length=20, default="",blank=False)
    total_amount =models.IntegerField(default=0 )
    Payment_Status =models.CharField(max_length=30,choices=PaymentStatus.choices ,default=PaymentStatus.UNPAID)
    payment_mod = models.CharField(max_length=30 ,choices=PaymentMod.choices,default=PaymentMod.CARD)
    status = models.CharField(max_length=60, choices=OrderStatus.choices ,default=OrderStatus.PROCCESSING)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name




