from EcommApp.models.product import Product
from django.shortcuts import render,get_object_or_404



def product_detail(request, product_id):
    # Get the current product
    product = get_object_or_404(Product, id=product_id)

    # Fetch related products from the same category, excluding the current product
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)

    # Pass the product and related products to the template
    context = {
        'product': product,
        'related_products': related_products,
        'category': product.category,
    }
    return render(request, 'productDetails.html', context)