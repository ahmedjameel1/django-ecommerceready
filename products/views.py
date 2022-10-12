from django.shortcuts import render 
from . models import Product
from carts.models import Cart
from carts.views import _cart_id
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def home(request):
    products = Product.objects.all()
    ctx = {'products':products}
    return render(request, 'homepage.html', ctx)


def product(request, product_id):
    sproduct = Product.objects.get(id=product_id)
    products = Product.objects.all()
    colors = sproduct.variations_set.colors()
    capacity = sproduct.variations_set.capacities()
    cart = None
    cartitems = None
    productslist = []
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cartitems = cart.cartitem_set.filter(cart=cart, is_active=True)
        for i in cartitems:
            productslist.append(i.product)
    except ObjectDoesNotExist:
        pass
    ctx = {'productslist':productslist, 'sproduct':sproduct
        ,'products':products,'colors':colors,'capacity':capacity}
    return render(request, 'products/productdetail.html', ctx)