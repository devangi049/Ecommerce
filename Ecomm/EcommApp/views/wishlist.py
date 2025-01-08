from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse
from EcommApp.views.wishlist_utility import get_or_create_wishlist
from django.shortcuts import get_object_or_404
from EcommApp.models.wishlist import WishlistItem
from EcommApp.models.cart import Cart,CartItem
from EcommApp.models.product import Product


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
    if not request.session.get('user_id'):
        messages.error(request, "Please log in to clear your wishlist.")
        return redirect('login')

    wishlist = get_or_create_wishlist(request.session['user_email'])

    if wishlist:
        wishlist.items.all().delete()  
        messages.success(request, "Your wishlist has been cleared.")
    else:
        messages.error(request, "Wishlist not found.")

    return redirect('wishlist') 

def add_to_cart_wishlist(request, product_id):
    if not request.session.get('user_id'):
        messages.error(request, "Please log in to add items to your cart.")
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    user_email = request.session['user_email']

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user_email=user_email)

    # Check if the item is already in the cart
    cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if cart_item_created:
        cart_item.quantity = 1  # Set default quantity for new cart item
        cart_item.save()
        messages.success(request, f"{product.name} has been added to your cart.")
    else:
        cart_item.quantity += 1  # Increment quantity if the item already exists in the cart
        cart_item.save()
        messages.info(request, f"Quantity for {product.name} has been updated in your cart.")

    # Remove the item from the wishlist
    wishlist = get_or_create_wishlist(user_email)
    wishlist_item = WishlistItem.objects.filter(wishlist=wishlist, product=product).first()
    print("not fremove wishlsit item")
    if wishlist_item:
        print("remove wishlsit")
        wishlist_item.delete()
        messages.info(request, f"{product.name} has been removed from your wishlist.")

    return redirect('cart')