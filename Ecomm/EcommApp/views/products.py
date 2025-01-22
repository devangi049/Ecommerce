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

    # Step 1: Get all products regardless of category first
    all_products = Product.get_all_products()  # Get all products by default

    # Step 2: Apply price filter if both min_price and max_price are provided
    try:
        if min_price:
            min_price = float(min_price)
            all_products = all_products.filter(discount__gte=min_price)  # Filter by minimum price
        if max_price:
            max_price = float(max_price)
            all_products = all_products.filter(discount__lte=max_price)  # Filter by maximum price
    except ValueError:
        # Handle invalid input gracefully
        min_price = None
        max_price = None

    # Step 3: If a category is selected, filter products by the selected category
    if category_id:
        try:
            category_id = int(category_id)  # Ensure the category_id is a valid integer
            all_products = all_products.filter(category_id=category_id)  # Filter products by selected category
        except ValueError:
            pass  # If category_id is invalid, ignore it (default to no category filter)

    # Step 4: Apply "new" and "in-stock" filters if applicable
    if is_new == "true":
        all_products = all_products.filter(is_new=True)
    if is_in_stock == "true":
        all_products = all_products.filter(is_in_stock=True)

    # Step 5: Paginate the filtered products
    paginator = Paginator(all_products, 9)  # Show 9 products per page
    page_number = request.GET.get('page')  # Get the current page number from the query parameters
    page_obj = paginator.get_page(page_number)

    # Step 6: Pass data to the template
    data = {
        'products': page_obj,  # Use the paginated products
        'categories': categories,
        'selected_category': category_id,  # Pass selected category ID for pre-selection in the UI
        'min_price': min_price,
        'max_price': max_price,
        'is_new': is_new,
        'is_in_stock': is_in_stock,
        'page_obj': page_obj
    }
    return render(request, 'products.html', data)
