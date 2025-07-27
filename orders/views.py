from django.forms import Form
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import razorpay
from product.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from cart.models import Cart, CartItem
from .forms import ShippingForm

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def payment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_items = Cart.objects.filter(user=request.user)
    
    # Initialize Razorpay client
    razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Create Razorpay order (amount in paise)
    razorpay_order = razorpay_client.order.create({
        "amount": int(product.price * 100),
        "currency": "INR",
        "payment_capture": "1",
    })

    context = {
        'product': product,
        'amount': product.price,
        'order_id': razorpay_order['id'],
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    }
    return render(request, 'orders/payment.html', context)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

def track_order(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'), 
        id=order_id, 
        user=request.user
    )
    return render(request, 'track_order.html', {'order': order})
@login_required
def start_payment(request):
    try:
        cart = Cart.objects.prefetch_related('items__product').get(user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items.exists():
            return HttpResponse("Cart is empty.")

        total_amount = sum(item.total_price for item in cart_items)

        if request.method == 'POST':
            form = ShippingForm(request.POST)
            if form.is_valid():
                shipping_data = form.cleaned_data

                razorpay_order = razorpay_client.order.create({
                    "amount": int(total_amount * 100),
                    "currency": "INR", 
                    "payment_capture": "1",
                })

                # Create Order with shipping details
                order = Order.objects.create(
                    user=request.user,
                    total_amount=total_amount,
                    payment_id=razorpay_order["id"],
                    shipping_name=shipping_data.get('full_name'),
                    shipping_address=shipping_data.get('address'),
                    state=shipping_data.get('state'),
                    city=shipping_data.get('city'),
                    pin_code=shipping_data.get('pin_code'),
                    contact_number=shipping_data.get('contact_number'),
                    order_status='Pending'
                )

                # Create OrderItems from CartItems
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price,
                        total_price=cart_item.total_price
                    )

                # Clear cart but keep the cart object
                cart.items.all().delete()

                context = {
                    "order": order,
                    "order_items": order.items.all(),
                    "amount": total_amount,
                    "order_id": razorpay_order["id"],
                    "razorpay_key": settings.RAZORPAY_KEY_ID,
                    "shipping_data": {
                        'name': order.shipping_name,
                        'address': order.shipping_address,
                        'state': order.state,
                        'city': order.city,
                        'pin_code': order.pin_code,
                        'contact': order.contact_number
                    }
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

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature,
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            order = get_object_or_404(Order, payment_id=razorpay_order_id)
            order.order_status = 'Confirmed'
            order.save()
            
            context = {
                'order': order,
                'order_items': order.items.all(),
                'payment_id': razorpay_payment_id,
                'shipping_data': {
                    'name': order.shipping_name,
                    'address': order.shipping_address,
                    'state': order.state,
                    'city': order.city,
                    'pin_code': order.pin_code,
                    'contact': order.contact_number
                }
            }
            return render(request, "success.html", context)
        except razorpay.errors.SignatureVerificationError:
            return HttpResponse("Payment verification failed.", status=400)

    return JsonResponse({"error": "Invalid request method."}, status=400)