# from django.shortcuts import render
# from EcommApp.models.category import Category
# from EcommApp.models.product import Product

# def product(request):
#     # Get all categories
#     categories = Category.get_all_categories()
#     # print("Categories:", categories)

#     # Get category_id from request
#     category_id = request.GET.get('category')
#     # print("category_id from request:", category_id)

#     # Fetch products based on category_id
#     if category_id:
#         all_products = Product.get_all_products_by_categories_id(category_id)
#         # print("Filtered products with category_id:", category_id, all_products)
#     else:
#         all_products = Product.get_all_products()
#         # print("All products:", all_products)

#     # Prepare data for the template
#     data = {
#         'products': all_products,
#         'categories': categories
#     }

#     return render(request, 'products.html', data)
from django.shortcuts import render
from EcommApp.models.category import Category
from EcommApp.models.product import Product
def product(request):
 
    categories = Category.get_all_categories()
    category_id = request.GET.get('category')  

    if category_id:
        all_products = Product.get_all_products_by_categories_id(category_id)
    else:
        all_products = Product.get_all_products()
 

    data = {
        'products': all_products,
        'categories': categories
    }

    return render(request,'products.html',data)