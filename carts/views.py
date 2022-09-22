from django.shortcuts import render, redirect
from . models import Cart, CartItem
from products.models import Product
from django.http import HttpResponse


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create() 
    return cart


def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    print(product)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))   
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()
    
    try:
        cartitem = CartItem.objects.get(product=product, cart=cart)
        cartitem.qty += 1
    except CartItem.DoesNotExist:
        cartitem = CartItem.objects.create(product=product, cart=cart,qty=1)
        cartitem.save()
        print(cartitem)
        return redirect('cart')

def cart(request):
    return render(request,'carts/cart.html')