from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', item_list, name='home'),
    path('product/<str:slug>/', GetProduct.as_view(), name='product'),
    path('shop/', Shop.as_view(), name='shop'),
    path('shop/<str:slug>/', Shop.as_view(), name='category'),
    path('add-to-cart/<str:slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<str:slug>/', remove_from_card, name='remove-from-cart'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('login/', user_login, name='login'),
    path('cart/', OrderSummaryView.as_view(), name='cart'),
]
