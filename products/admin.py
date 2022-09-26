from django.contrib import admin
from . models import Product , Variations

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'stock', 'created', 'price', 'modified', 'is_active')
    prepopulated_fields = {'slug':('title',)}

class VariationsAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'is_active')
    list_editable= ('is_active',)
    list_filter  = ('product', 'variation_category', 'is_active')
    
    
    
admin.site.register(Product,ProductAdmin)
admin.site.register(Variations,VariationsAdmin)