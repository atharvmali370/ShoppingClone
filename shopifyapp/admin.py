from django.contrib import admin
from shopifyapp.models import Product, Category , Cart, CartItem

# Register your models here.

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     exclude = ('name','discription')


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     fields = ('name','discription')



admin.site.register(Product)
admin.site.register(Category)

admin.site.register(Cart)
admin.site.register(CartItem)

