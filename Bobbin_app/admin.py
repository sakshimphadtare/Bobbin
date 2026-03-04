from django.contrib import admin
from .models import Product, ProductImage, WishlistItem, CartItem, UserPincode, Review

class ProductImageInline(admin.TabularInline):  # or use admin.StackedInline
    model = ProductImage
    extra = 3  # Show 3 empty image upload slots by default
    max_num = 10  # Optional: limit to 10 images
    fields = ['image', 'alt_text']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'category']
    list_filter = ['category', 'material', 'color', 'size']
    search_fields = ['name', 'brand']
    inlines = [ProductImageInline]  # ✅ Attach multiple image upload option here

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'alt_text']

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'size']

# ✅ Added the missing models for completeness
@admin.register(UserPincode)
class UserPincodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'pincode', 'address']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'comment', 'created_at']
