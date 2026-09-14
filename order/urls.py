from django.contrib import admin
from django.urls import path , include
from . import views


urlpatterns =[
        path('order/new/', views.new_order,name='order'),
        path('order/', views.get_orders,name='get_orders'),
        path('order/<str:pk>/', views.get_order,name='get_order'),
        path('order/<str:pk>/process', views.update_status_order,name='update_status_order'),
        path('order/<str:pk>/delete', views.delete_order,name='delete_order'),

] 