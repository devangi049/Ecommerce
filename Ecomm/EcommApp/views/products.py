from django.shortcuts import render
from EcommApp.models.category import Category
from django.core.paginator import Paginator
from EcommApp.models.product import Product

def product(request):
    categories = Category.get_all_categories()
    category_id = request.GET.get('category')  
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    is_new = request.GET.get('is_new')  # Filter for new products
    is_in_stock = request.GET.get('is_in_stock')  # Filter for in-stock products
    # products = Product.objects.all()


    # paginator = Paginator(products, 9)  # Show 9 products per page
    # page_number = request.GET.get('page')  # Get the current page number from the query parameters
    # page_obj = paginator.get_page(page_number) 
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

    # Apply new and in-stock filters
    if is_new == "true":
        all_products = all_products.filter(is_new=True)
    if is_in_stock == "true":
        all_products = all_products.filter(is_in_stock=True)
    paginator = Paginator(all_products, 9)  # Show 9 products per page
    page_number = request.GET.get('page')  # Get the current page number from the query parameters
    page_obj = paginator.get_page(page_number) 
    data = {
        'products': all_products,
        'categories': categories,
        'min_price': min_price,
        'max_price': max_price,
        'is_new': is_new,
        'is_in_stock': is_in_stock,
        'page_obj': page_obj
    }
    return render(request, 'products.html', data)


