from django.contrib import admin
from orders.models import *

# Register your models here.
class OrderProductInlineAdmin(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ['payment','product','product_price','user','quantity','variations']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'created_at', 'is_ordered','status',]
    inlines = [OrderProductInlineAdmin]
    

admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)