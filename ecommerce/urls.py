from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', item_list, name='item-list'),
    path('product/<str:slug>', GetProduct.as_view(), name='product'),
    path('shop/', shop, name='shop'),
    path('cart/', cart, name='cart'),

]
