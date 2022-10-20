from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib import messages, auth
from accounts.models import Account 
from django.contrib.auth import authenticate 
#verify account
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.views import _cart_id
from carts.models import Cart, CartItem
# Create your views here.

def register(request):  
    if request.user.is_authenticated:
        return redirect('home') 
    if request.method == "POST":  
        updated_request = request.POST.copy()
        updated_request.update({'username': request.POST['email']})
        form = RegistrationForm(updated_request)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            phone_number = form.cleaned_data["phone_number"]
            username = form.cleaned_data["username"].split("@")[0]
            user = Account.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    username = username
                )
            user.phone_number = phone_number
            user.save()
            current_site=get_current_site(request)
            mail_subject = "Activate your account to ecommerceready!"
            message = render_to_string("accounts/account_verification.html",
            {
            'user' : user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message ,to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()       
    return render(request,'accounts/register.html',{'form':form})

def login(request):   
    if request.user.is_authenticated:
        return redirect('home') 
    if request.method == "POST":
        form = LoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_active == True:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items_exist = CartItem.objects.filter(cart=cart).exists()
                if cart_items_exist:
                    cart_items = CartItem.objects.filter(cart=cart)
                    # GETTING THE PRODUCT VARIATION BY CART ID
                    product_variation = []
                    for item in cart_items:
                        variation = item.variation.all()
                        product_variation.append(list(variation))

                    # GET THE CART ITEMS FROM THE USER
                    cart_items = CartItem.objects.filter(user=user)
                    existing_variation_list = []
                    cart_item_id = []
                    for item in cart_items:
                        existing_variation = item.variation.all()
                        existing_variation_list.append(list(existing_variation))
                        cart_item_id.append(item.id)

                    for product in product_variation:
                        if product in existing_variation_list:
                            index = existing_variation_list.index(product)
                            item_id = cart_item_id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.qty += 1
                            item.user = user
                            item.save()
                        else:
                            cart_items = CartItem.objects.filter(cart=cart)
                            for item in cart_items:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request,user)
            messages.success(request,'Welcome '+ request.user.username+'!')
            return redirect('home')
        else:
            messages.warning(request, 'Invaldi username or password is incorrect!')
    else:
        form = LoginForm()      
    return render(request,'accounts/login.html',{'form':form})


def logout(request):
    auth.logout(request)
    messages.info(request,'Logged Out!')
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user= Account._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user != None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account Activated Successfully!')
        return redirect('login')
    else:
        messages.info(request,'Link Expired!')
        return redirect('register')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site=get_current_site(request)
            mail_subject = "Reset Your Password!"
            message = render_to_string("accounts/forgotpasswordemail.html",
            {
            'user' : user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message ,to=[to_email])
            send_email.send()
            messages.success(request, 'An Email with instructions sent to your emailaddress!')
        else:
            messages.error(request, 'Enter a Valid EmailAdress!')
    return render(request, 'accounts/forgotpassword.html')


def resetPassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user != None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('resetPassword')
    else:
        messages.info(request,'Expired Link!')
        return redirect('login')



def resetPassword(request):
    if request.method == "POST":
        password = request.POST['enterpassword']
        confirm  = request.POST['confirmpassword']

        if password == confirm:
            uid = request.session.get('uid')
            user= Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Success!')
            return redirect('login')
        else:
            messages.info(request, 'Password doesn\'t match!')
            return redirect('resetPassword')

    return render(request, 'accounts/resetPassword.html')