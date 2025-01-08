from EcommApp.models.wishlist import Wishlist
from EcommApp.models.user import User

def get_or_create_wishlist(user_email):
    user = User.objects.get(email=user_email)
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    return wishlist