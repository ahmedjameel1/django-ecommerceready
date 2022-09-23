from django.shortcuts import render 
from . models import Product
from carts.models import Cart
from carts.views import _cart_id
# Create your views here.

def home(request):
    products = Product.objects.all()
    ctx = {'products': products}
    return render(request, 'homepage.html', ctx)


def product(request, product_id):
    sproduct = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cartitems = cart.cartitem_set.filter(cart=cart, is_active=True)
    productslist = []
    for i in cartitems:
        productslist.append(i.product)
    ctx = {'productslist':productslist, 'sproduct':sproduct}
    return render(request, 'products/productdetail.html', ctx)