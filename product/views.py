from django.shortcuts import render, get_object_or_404
from .models import Product
from .models import Category
from django.db.models import Q

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'product_list.html', {
        'category': category,
        'products': products
    })

def product_list(request):
    products = Product.objects.all()
    query = request.GET.get('q', '')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'product_list.html', {'products': products, 'query': query})



def product_detail(request, product_id):
    # Fetch the product from the database using the product_id
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_details.html', {'product': product})

def shipping_policy(request):
    return render(request, 'shipping_policy.html')

