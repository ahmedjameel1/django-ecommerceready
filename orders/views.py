from django.shortcuts import render, redirect
from carts.models import CartItem , Cart
from .forms import OrderForm , Order
import datetime
from .models import Payment
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def placeOrder(request):
    current_user = request.user
    cartitems = CartItem.objects.filter(user=current_user)
    price = 0 
    for item in cartitems:
        price += item.product.price*item.qty
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.email = form.cleaned_data['email']
            data.order_total = price
            data.tax = data.order_total * 10 / 100
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.user = current_user
            order_grand = data.order_total + data.tax
            data.save()

            order = Order.objects.get(user=current_user,
                                      is_ordered = False,
                                      order_number=order_number)
    
    ctx = {'order':order,'cartitems':cartitems,'order_grand':order_grand}
    return render(request, 'orders/place_order.html',ctx)

def paymentSuccess(request):
    current_user = request.user
    cartitems = CartItem.objects.filter(user=current_user)
    price = 0 
    for item in cartitems:
        price += item.product.price*item.qty
    order = Order.objects.get(user=current_user,is_ordered = False)
    tax = price * 10 / 100
    order_grand = price + tax
    yr = int(datetime.date.today().strftime('%Y'))
    dt = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))
    d = datetime.date(yr,mt,dt)
    current_date = d.strftime("%Y%m%d")
    payment_id = current_date + str(order.id) + current_date
    payment_method = 'PayPal'
    amount_paid = order_grand
    payment = Payment.objects.create(user=current_user,
    payment_id=payment_id,payment_method=payment_method,amount_paid=amount_paid,
    status='Accepted')
    order.payment = payment
    order.save()
    current_site=get_current_site(request)
    mail_subject = "Payment Success!"
    email = order.user.email
    message = render_to_string("orders/orderaccepted.html",
    {
    'user' : current_user,
    'domain':current_site,
    'ordernumber':order.order_number,
    })
    to_email = email
    send_email = EmailMessage(mail_subject, message ,to=[to_email])
    send_email.send()
    order.is_ordered = True
    order.status = 'Accepted'
    order.save()
    cart = CartItem.objects.filter(user=current_user)
    for item in cart:
        item.delete()
        item.product.stock -= item.qty
        item.product.save()
        
    ctx = {'order':order,'cartitems':cartitems,'order_grand':order_grand
    ,'tax':tax}
    return render(request, 'orders/paymentsuccess.html',ctx)