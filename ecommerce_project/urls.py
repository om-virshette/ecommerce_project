"""
URL configuration for ecommerce_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import render
from product.views import shipping_policy
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('home/', include('product.urls')),
    path('', include('product.urls')),
    path('orders/', include('orders.urls')),
    path('shipping-policy/', shipping_policy, name='shipping_policy'),
    path('return-policy/', include('return_policy.urls')),  # Assuming return_policy is in policies app
    path('policies/', include('policies.urls')),
    path('faq/', include('faq_section.urls')),
    path('terms/', include('tos.urls')),
    path('contact/', include('contact.urls')),
    path('about/', include('about.urls')), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
