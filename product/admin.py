from django.contrib import admin
from .models import Cart , CartItem, Product

# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['i_user']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['i_cart','i_product']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "description" ,'stock', 'price']
