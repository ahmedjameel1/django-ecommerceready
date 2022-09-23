from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name = 'cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name = 'addcart'),
    path('decrease_cart/<int:product_id>/', views.decrease_cart, name = 'decreasecart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name = 'removecart'),


]
