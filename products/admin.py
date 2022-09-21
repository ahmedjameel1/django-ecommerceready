from django.contrib import admin
from . models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'stock', 'created', 'price', 'modified', 'is_active')
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Product,ProductAdmin)
