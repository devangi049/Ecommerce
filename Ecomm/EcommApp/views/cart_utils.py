from EcommApp.models.cart import Cart
from EcommApp.models.user import User
def get_or_create_cart(user_email):
    user = User.objects.get(email=user_email)
    cart, created = Cart.objects.get_or_create(user=user)
    return cart 