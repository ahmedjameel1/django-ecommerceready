from django.db import models
from accounts.models import Account
from products.models import Product as Pro

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Pro, on_delete=models.CASCADE, null=True)
    qty = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.product.title)
    
    def cartItemPrice(self):
        return int(self.product.price*self.qty)
    
    