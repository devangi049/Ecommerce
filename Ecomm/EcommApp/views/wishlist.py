from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse
from EcommApp.views.wishlist_utility import get_or_create_wishlist
from django.shortcuts import get_object_or_404
from EcommApp.models.wishlist import WishlistItem
from EcommApp.models.cart import Cart,CartItem
from EcommApp.models.product import Product
from EcommApp.views.cart_utils import get_or_create_cart
from EcommApp.models.user import User


def Wishlist(request):
    if not request.session['user_id']:
        messages.error(request, "Please log in to view your cart.")
        return redirect('login')
    
    
    wishlist = get_or_create_wishlist(request.session['user_email'])
    wishlist_items = wishlist.items.all()

    return render(request,"wishlist.html",{"wishlist_items": wishlist_items})



def add_to_wishlist(request, product_id):
    if not request.session.get('user_id'):
        messages.error(request, "Please log in to add items to your wishlist.")
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    wishlist = get_or_create_wishlist(request.session['user_email'])

    wishlist_item = WishlistItem.objects.filter(wishlist=wishlist, product=product).first()
    if wishlist_item:
        messages.error(request, f"{product.name} is already in your wishlist.")
    else:
        WishlistItem.objects.create(wishlist=wishlist, product=product)
        messages.success(request, f"{product.name} has been added to your wishlist.")
    return redirect('product')


def remove_from_wishlist(request, product_id):
    if not request.session.get('user_id'):
        messages.error(request, "Please log in to remove items from your wishlist.")
        return redirect('login')

    wishlist = get_or_create_wishlist(request.session['user_email'])
    wishlist_item = WishlistItem.objects.filter(wishlist=wishlist, product_id=product_id).first()

    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, "Item removed from your wishlist.")
    else:
        messages.error(request, "Item not found in your wishlist.")
    return redirect('wishlist')


def wishlist(request):
    user_email = request.session.get('user_email')
    wishlist_items = WishlistItem.objects.filter(wishlist__user__email=user_email) if user_email else []

    context = {
        'wishlist_items': wishlist_items,
        'total_price': sum(item.product.discount * (item.quantity if hasattr(item, 'quantity') else 1) for item in wishlist_items),
    }
    return render(request, 'wishlist.html', context)

def clear_wishlist(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to perform this action.")
        return redirect('login')

    WishlistItem.objects.filter(user=request.user).delete()
    messages.success(request, "Your wishlist has been cleared.")
    return redirect('wishlist')

def add_to_cart_wishlist(request, product_id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to perform this action.")
        return redirect('login')

    # Get the user email from the session
    user_email = request.session.get('user_email')
    if not user_email:
        messages.error(request, "User email is missing. Please log in again.")
        return redirect('login')

    # Get or create the cart for the user
    user = User.objects.get(email=user_email)
    cart, created = Cart.objects.get_or_create(user=user)

    # Get the product
    product = get_object_or_404(Product, id=product_id)

    # Add the product to the cart
    cart_item, cart_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not cart_created:
        cart_item.quantity += 1  # Increment quantity if the product already exists
        cart_item.save()

    # Remove the product from the wishlist
    wishlist = get_or_create_wishlist(user_email)
    wishlist_item = WishlistItem.objects.filter(wishlist=wishlist, product=product).first()
    if wishlist_item:
        wishlist_item.delete()

    messages.success(request, f"{product.name} was added to your cart and removed from the wishlist.")
    return redirect('wishlist')
