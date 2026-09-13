from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User

# Create your models here.


class Category(models.TextChoices):
    COMPUTERS = "Computers"
    FOODS = "Foods"
    KIDS = "Kids"
    HOME = "Home"
    ANIMALS = "Animals"
    SPORTS = "Sports"
    SCHOOL = "School"
    CLOTHES = "Clothes"
    VEHICLES = "Vehicles"
    MUSIC = "Music"


class Product(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=1000, default="", blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    brand = models.CharField(max_length=200, default="", blank=False)
    category = models.CharField(max_length=40, blank=False, choices=Category.choices)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return (self.name)
    @property
    def average_rating(self):
        result = self.reviews.aggregate(avg=Avg('rating'))
    # result = {'avg': 4.0}  أو  {'avg': None} لو مفيش reviews
        return result['avg'] or 0







class Review(models.Model):
    product = models.ForeignKey(Product,null=True,on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(default= 0)
    comment = models.TextField(max_length=1000, default="", blank=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return (self.comment)