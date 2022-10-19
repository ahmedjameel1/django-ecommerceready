from carts.views import _cart_id
from carts.models import Cart , CartItem

def cart_processor(request):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cartitems = CartItem.objects.filter(cart=cart)
    price = 0
    count = 0
    for cartitem in cartitems:
        count += cartitem.qty
        price += cartitem.product.price*cartitem.qty
    return {'price':price,'count':count}