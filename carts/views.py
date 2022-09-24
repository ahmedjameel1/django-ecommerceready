from django.shortcuts import render, redirect
from . models import Cart, CartItem
from products.models import Product
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create() 
    return cart


def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))   
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()
    
    cartitem = CartItem.objects.filter(cart=cart, product=product).exists()
    if cartitem == True:
        cartitem = CartItem.objects.get(cart=cart, product=product)
        cartitem.qty += 1 
        cartitem.save()
    else:
        cartitem = CartItem.objects.create(
            cart=cart,
            product=product,
            qty=1
        ) 
        cartitem.save()
    return redirect('cart')


def decrease_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cartitem = CartItem.objects.filter(cart=cart, product=product).exists()
    if cartitem == True:
        cartitem = CartItem.objects.get(cart=cart, product=product)
        if cartitem.qty > 1:
            cartitem.qty -= 1 
            cartitem.save()
        else:
            cartitem.delete()
            cart.save()
    return redirect('cart')

def remove_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cartitem = CartItem.objects.get(product=product, cart=cart)
    cartitem.delete()
    cart.save()
    return redirect('cart')


def cart(request):
    print(request.path)
    cart = None
    cartitems = None
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cartitems = cart.cartitem_set.filter(cart=cart,is_active=True).order_by('-qty')
    except ObjectDoesNotExist:
        pass
    ctx = {'cart':cart,'cartitems':cartitems}
    return render(request,'carts/cart.html', ctx)