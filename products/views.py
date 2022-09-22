from django.shortcuts import render 
from . models import Product
# Create your views here.

def home(request):
    products = Product.objects.all()
    ctx = {'products': products}
    return render(request, 'homepage.html', ctx)