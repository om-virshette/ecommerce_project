from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.order_history, name='order_history'),
    path('track/<int:order_id>/', views.track_order, name='track_order'),
    path('payment/success/', views.payment_success, name='payment_success'),

    path('start-payment/', views.start_payment, name='start_payment'),
]
