from math import prod
from django.shortcuts import HttpResponse, render, redirect
from . models import Cart, CartItem
from products.models import Product, Variations
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create() 
    return cart


def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    product_variations = []
    if request.method == 'POST':
        for item in request.POST:
            key = item 
            value = request.POST[key]
            try:
                variation = Variations.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variations.append(variation) 
            except:
                pass
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))   
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()
    
    ex_variation = []
    id = []
    ifcartitem = CartItem.objects.filter(cart=cart,product=product).exists
    if ifcartitem:
        cartitem = CartItem.objects.filter(cart=cart,product=product)
        for item in cartitem:
            ex_vars = item.variation.all()
            ex_variation.append(list(ex_vars))
            id.append(item.id)
        if product_variations in ex_variation:
            index = ex_variation.index(product_variations)
            print(index)
            item_id = id[index]
            print(item_id)
            item = CartItem.objects.get(product=product, id=item_id)
            item.qty += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, cart=cart, qty=1)
            if len(product_variations) > 0:
                item.variation.clear()           
                item.variation.add(*product_variations)
            item.save()
    else:
        cartitem = CartItem.objects.create(
            cart=cart,
            product=product,
            qty=1
        ) 
        if len(product_variations) > 0:
            cartitem.variation.clear()           
            cartitem.variation.add(*product_variations)
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
    cart = None
    cartitems = None
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cartitems = cart.cartitem_set.filter(cart=cart,is_active=True).order_by('-qty')
    except ObjectDoesNotExist:
        pass
    ctx = {'cart':cart,'cartitems':cartitems}
    return render(request,'carts/cart.html', ctx)