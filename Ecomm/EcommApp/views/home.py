# views.py
from django.shortcuts import redirect, render
from django.views import View
from EcommApp.models.category import Category
from EcommApp.models.product import Product

class Index(View):
    def get(self, request, category_id=None):
        categories = Category.get_all_categories()
        category_id = category_id  # Fetch from URL parameter
        is_new = request.GET.get('is_new')  # Filter for new products
        is_in_stock = request.GET.get('is_in_stock')  # Filter for in-stock products

        # Filter products based on category_id
        if category_id:
            all_products = Product.get_all_products_by_categories_id(category_id)
        else:
            all_products = Product.get_all_products()

        # Apply additional filters
        if is_new == "true":
            all_products = all_products.filter(is_new=True)
        if is_in_stock == "true":
            all_products = all_products.filter(is_in_stock=True)

        data = {
            'products': all_products,
            'categories': categories,
            'selected_category_id': category_id,
        }
        return render(request, "index.html", data)
