from django.shortcuts import render
from EcommApp.models.category import Category
from django.core.paginator import Paginator
from EcommApp.models.product import Product

def product(request):
    categories = Category.get_all_categories()  # Retrieve all categories
    category_id = request.GET.get('category')  # Get selected category ID
    min_price = request.GET.get('min_price')  # Get minimum price filter
    max_price = request.GET.get('max_price')  # Get maximum price filter
    is_new = request.GET.get('is_new')  # Filter for new products
    is_in_stock = request.GET.get('is_in_stock')  # Filter for in-stock products

    # Step 1: Filter products by selected category
    all_products = Product.get_all_products()
    if category_id:
        try:
            category_id = int(category_id)
            all_products = all_products.filter(category_id=category_id)
        except ValueError:
            pass  # Ignore invalid category ID

    # Step 2: Apply price filter if both min_price and max_price are provided
    try:
        if min_price:
            min_price = float(min_price)
            all_products = all_products.filter(discount__gte=min_price)
        if max_price:
            max_price = float(max_price)
            all_products = all_products.filter(discount__lte=max_price)
    except ValueError:
        min_price = None
        max_price = None

    # Step 3: Apply "new" and "in-stock" filters within the selected category
    if is_new == "true":
        all_products = all_products.filter(is_new=True)
    if is_in_stock == "true":
        all_products = all_products.filter(is_in_stock=True)

    # Step 4: Paginate the filtered products
    paginator = Paginator(all_products, 9)  # Show 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Step 5: Pass data to the template
    data = {
        'products': page_obj,  # Use paginated products
        'categories': categories,
        'selected_category': category_id,  # For UI pre-selection
        'min_price': min_price,
        'max_price': max_price,
        'is_new': is_new,
        'is_in_stock': is_in_stock,
        'page_obj': page_obj
    }
    return render(request, 'products.html', data)
