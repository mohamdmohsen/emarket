from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('userinfo/',views.current_user,name='info'),
    path('userinfo/update/',views.update_user,name='info_update'),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('reset_password/<str:token>/',views.reset_password,name='reset_password'),
]
