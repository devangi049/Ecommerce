from django.shortcuts import render
from EcommApp.models.category import Category
from EcommApp.models.product import Product

def product(request):
    categories = Category.get_all_categories()
    category_id = request.GET.get('category')  
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Filter products by category
    if category_id:
        all_products = Product.get_all_products_by_categories_id(category_id)
    else:
        all_products = Product.get_all_products()

    # Apply price filter if min_price or max_price is provided
    try:
        if min_price:
            min_price = float(min_price)
            all_products = all_products.filter(discount__gte=min_price)  # Filter products with price >= min_price
        if max_price:
            max_price = float(max_price)
            all_products = all_products.filter(discount__lte=max_price)  # Filter products with price <= max_price
    except ValueError:
        min_price = None
        max_price = None

    data = {
        'products': all_products,
        'categories': categories,
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, 'products.html', data)
