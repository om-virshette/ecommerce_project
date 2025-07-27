from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.forms import ShippingForm
from product.models import Product
from .models import Cart, CartItem
from django.conf import settings
import razorpay
from orders.models import Order  # You should have this

# Razorpay client setup
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def view_cart(request):
    # Get or create user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Get all items in the cart
    cart_items = cart.items.all()
    # Calculate total (can also use sum(item.total_price) since you have that field)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    
    return render(request, 'view_cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_amount': total_amount
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Get or create user's cart
    cart, cart_created = Cart.objects.get_or_create(user=request.user)
    
    # Check if product already in cart
    cart_item = cart.items.filter(product=product).first()
    
    if cart_item:
        # Product exists in cart - increment quantity
        cart_item.quantity += 1
        cart_item.save()
    else:
        # Product not in cart - add new item
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1
        )
    
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    # Verify the item belongs to the user's cart
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('view_cart')

@login_required
def start_payment(request):
    try:
        # Get the user's cart with prefetched items and products
        cart = Cart.objects.prefetch_related('items__product').get(user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items.exists():
            return HttpResponse("Cart is empty.")

        # Correct way to calculate total (using CartItem's product relationship)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        # Or alternatively use the pre-calculated total_price:
        # total_amount = sum(item.total_price for item in cart_items)

        if request.method == 'POST':
            form = ShippingForm(request.POST)
            if form.is_valid():
                shipping_data = form.cleaned_data
                request.session['shipping_data'] = shipping_data

                razorpay_order = razorpay_client.order.create({
                    "amount": int(total_amount * 100),
                    "currency": "INR",
                    "payment_capture": "1",
                })

                # Create Order instance
                order = Order.objects.create(
                    user=request.user,
                    total_amount=total_amount,
                    payment_id=razorpay_order["id"],
                    shipping_name=shipping_data.get('full_name'),
                    contact_number=shipping_data.get('contact_number'),
                    shipping_address=shipping_data.get('address'),
                    state=shipping_data.get('state'),
                    city=shipping_data.get('city'),
                    pin_code=shipping_data.get('pin_code'),
                )

                # Add items to order (assuming Order has items field)
                order.items.set(cart_items)
                
                # Clear the cart
                cart.items.all().delete()

                context = {
                    "cart_items": cart_items,
                    "amount": total_amount,
                    "order_id": razorpay_order["id"],
                    "razorpay_key": settings.RAZORPAY_KEY_ID,
                    "shipping_data": shipping_data,
                }
                return render(request, "payment.html", context)

        else:
            form = ShippingForm()

        return render(request, "shipping.html", {
            "form": form,
            "cart_items": cart_items,
            "total_amount": total_amount,
        })

    except Cart.DoesNotExist:
        return HttpResponse("Cart not found.")
        
@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')


@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')