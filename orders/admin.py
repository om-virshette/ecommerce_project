from django.contrib import admin
from .models import Order,OrderItem
from django.utils.html import format_html

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity','total_price')
    can_delete = False
    fk_name = 'order'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount','order_status', 'created_at')
    list_filter = ('order_status','created_at')
    inlines = [OrderItemInline]
    search_fields = ('id','user__username', 'payment_id')
    readonly_fields = ('cart_items_display','created_at', 'payment_id','total_amount')
    date_hierarchy = 'created_at'
    fields = (
        'user', 'total_amount', 'payment_id', 'order_status',
        'shipping_address', 'shipping_name', 'state', 'city', 'pin_code',
        'contact_number', 'cart_items_display',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items__product')
    
    def cart_items_display(self, obj):
        if not obj.cart.exists():
            return "No items"
        return "\n".join([
            f"{item.product.title} x {item.quantity}" for item in obj.cart.all()
        ])
    
    cart_items_display.short_description = "Cart Items"