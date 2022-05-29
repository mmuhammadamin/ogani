from django.contrib import admin

from .models import WishList,Cart,CartItem,Order

class WishListAdmin(admin.ModelAdmin):
    filter_horizontal = ['product']

class CartListInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    inlines = [CartListInline]
admin.site.register(WishList,WishListAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Order)