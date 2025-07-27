from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<slug:category_slug>/', views.products_by_category, name='products_by_category'),
    path('shipping-policy/', views.shipping_policy, name='shipping_policy'),
]