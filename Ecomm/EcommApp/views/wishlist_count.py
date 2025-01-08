from EcommApp.views.wishlist_utility import get_or_create_wishlist



def Wishlist_Count(request):
    wishlist_count = 0

    if request.session.get('user_email'):
        wishlist = get_or_create_wishlist(request.session.get('user_email'))
        wishlist_count = wishlist.items.count() if wishlist else 0

    return {'wishlistCount': wishlist_count}

        