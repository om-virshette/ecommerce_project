from django.db import models
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart #{self.id} - {self.user.username}"

    @property
    def total_value(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,  # Changed to string reference
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'product.Product',  # Changed to string reference
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Calculate total_price before saving"""
        if not self.product_id:  # Ensure product exists
            raise ValueError("CartItem must have a product")
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.title if hasattr(self.product, 'title') else 'Product'} x {self.quantity}"

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"