from django.contrib import admin
from .models import Product, Category  # removed ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'created_at']
    list_filter  = ['category', 'available', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'available']
    # Removed ProductImageInline

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
