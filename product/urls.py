from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('product/',views.get_all_products,name='products'),
    path('product/<str:pk>/',views.get_string_products,name='string_products'),
    path('product/new',views.new_product,name='new_products'),
    path('product/update/<str:pk>/',views.update_product,name='update_products'),
    path('product/delete/<str:pk>/',views.delete_product,name='delete_products'),    
    path('product/<int:pk>/review/', views.create_review, name='create-review'),
]
