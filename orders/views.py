from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm , Order
import datetime
from .models import Payment
from django.contrib.auth.decorators import login_required


def placeOrder(request):
    return render(request, 'orders/place_order.html')

def paymentSuccess(request):
    return render(request, 'orders/paymentsuccess.html')