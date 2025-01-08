from EcommApp.views.cart_utils import get_or_create_cart

def Cart_Count(request):
    cart_count = 0

    if request.session.get('user_email'):  # Using 'user_email' from the session
        cart = get_or_create_cart(request.session.get('user_email'))
        cart_count = cart.items.count() if cart else 0

    return {'cartCount': cart_count}
