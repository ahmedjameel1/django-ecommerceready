from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . models import Cart, CartItem
from products.models import Product, Variations
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Account
# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create() 
    return cart


def add_cart(request,product_id):
    user = request.user
    cartitems = None
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
    if user.is_authenticated == False:
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

    else:
        cartitems = CartItem.objects.filter(user=user,product=product)
        ex_variation = []
        id = []
        ifcartitem = CartItem.objects.filter(user=user,product=product).exists
        if ifcartitem:
            cartitem = CartItem.objects.filter(user=user,product=product)
            for item in cartitem:
                ex_vars = item.variation.all()
                ex_variation.append(list(ex_vars))
                id.append(item.id)
            if product_variations in ex_variation:
                index = ex_variation.index(product_variations)
                print(index)
                item_id = id[index]
                print(item_id)
                item = CartItem.objects.get(product=product,user=user, id=item_id)
                item.qty += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, user=user, qty=1)
                if len(product_variations) > 0:
                    item.variation.clear()           
                    item.variation.add(*product_variations)
                item.save()
        else:
            cartitem = CartItem.objects.create(
                user=user,
                product=product,
                qty=1
            ) 
            if len(product_variations) > 0:
                cartitem.variation.clear()           
                cartitem.variation.add(*product_variations)
            cartitem.save()
    return redirect('cart')

def decrease_cart(request,product_id,cart_item_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    if user.is_authenticated == False:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        try:
            cartitem = CartItem.objects.get(cart=cart, product=product,id=cart_item_id)
            if cartitem.qty > 1:
                cartitem.qty -= 1 
                cartitem.save()
            else:
                cartitem.delete()
        except:
            pass
    else:
        cartitem = CartItem.objects.get(user=user,product=product,id=cart_item_id)
        if cartitem.qty > 1:
            cartitem.qty -= 1 
            cartitem.save()
        else:
            cartitem.delete()
    return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    product = Product.objects.get(id=product_id)
    user = request.user
    if user.is_authenticated == False:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        try:
            cartitem = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
            cartitem.delete()
            cart.save()
        except:
            pass
    else:
        cartitem = CartItem.objects.get(product=product, user=user,id=cart_item_id)
        cartitem.delete()
    return redirect('cart')


def cart(request):
    cart = None
    cartitems = None
    user = request.user
    if user.is_authenticated == False:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cartitems = cart.cartitem_set.all().order_by('-qty')
        except ObjectDoesNotExist:
            pass
    else:
        try:
            cartitems = CartItem.objects.filter(user=user).order_by('-qty')
        except ObjectDoesNotExist:
            pass
    ctx = {'cart':cart,'cartitems':cartitems}
    return render(request,'carts/cart.html', ctx)

@login_required(login_url='login')
def checkout(request):
    cart = None
    if request.user.is_authenticated == False:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    else:
        cartitems = CartItem.objects.filter(cart=cart)
        price = 0
        count = 0
        for cartitem in cartitems:
            count += cartitem.qty
            price += cartitem.product.price*cartitem.qty
    return render(request, 'carts/cartcheckout.html',{'cartitems':cartitems,'price':price
    ,'count':count})

