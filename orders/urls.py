from django.urls import path
from . import views

urlpatterns = [
   path('placeorder', views.placeOrder, name = 'placeorder'),
   path('success', views.paymentSuccess, name = 'paymentsuccess'),
]
