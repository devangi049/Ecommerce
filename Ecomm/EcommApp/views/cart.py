from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from EcommApp.models.product import Product
from EcommApp.views.cart_utils import get_or_create_cart
from django.http import JsonResponse
from EcommApp.models.cart import CartItem

def Cart(request):
    if not request.session['user_id']:
        messages.error(request,"Please log in to view your cart.")
        return redirect('login')
    
    cart = get_or_create_cart(request.session['user_email'])
    cart_items= cart.items.all()


  
    total_price = sum(item.product.discount * item.quantity for item in cart_items)
    return render(request,"cart.html",{"cart_items":cart_items},{"total_price":total_price})

def add_to_cart(request,product_id):
    if not request.session.get('user_id'):
        messages.error(request,"Please log in to add items to the cart.")
        return redirect('login')
    
    product = get_object_or_404(Product,id=product_id)
    cart=get_or_create_cart(request.session.get('user_email'))

    cart_item=CartItem.objects.filter(cart=cart,product=product).first()

    if cart_item:
        messages.error(request, f"{product.name} is already in your cart.")
    else:
        cart_item=CartItem(cart=cart,product=product,quantity=1)
        cart_item.save()
        messages.success(request, f"{product.name} has been added to your cart.")


    if 'from_product_detail' in request.GET:
        return redirect('product_detail',product_id=product.id)
    return redirect('product')

def cart_view(request):
    if not request.session.get('user_id'):
        return render(request, 'login.html', {"error": "Please log in to view your cart."})

    # Assuming `get_or_create_cart` fetches the cart for the logged-in user
    cart = get_or_create_cart(request.session['user_email'])
    cart_items = cart.items.all()
    
    # Calculate the total price
    total_price = sum(item.product.discount * item.quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def Remove_From_Cart(request,product_id):
    if not request.session.get('user_id'):
        messages.error(request,"Please log in to remove items from the cart.")
        return redirect('login')
    
    cart=get_or_create_cart(request.session.get('user_email'))

    if not cart:
        messages.error(request,"Cart not found.")
        return redirect('cart_view')
    cart_item=CartItem.objects.filter(cart=cart,product_id=product_id).first()

    if not cart_item:
        messages.error(request,"Item not found in cart.")
    else:
        cart_item.delete()
        messages.success(request, "Item removed from the cart.")

        return redirect('cart_view')
def increment_quantity(request, product_id):
    if not request.session.get('user_id'):
        messages.error(request, "Please log in to update your cart.")
        return redirect('login')
    
    # Get or create the cart
    cart = get_or_create_cart(request.session.get('user_email'))

    # Get the cart item for the given product
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

    if cart_item:
        # Increment the quantity
        cart_item.quantity += 1
        
        # Save the cart item
        cart_item.save()

        # Show success message
        messages.success(request, f"Updated quantity of {cart_item.product.name} to {cart_item.quantity}.")
    else:
        # If item not found in cart
        messages.error(request, "Item not found in your cart.")

    return redirect("cart_view")

def decrement_quantity(request,product_id):
    if not request.session.get('user_id'):
        messages.error(request,"Please log in to update your cart.")
        return redirect('login')
    
    cart=get_or_create_cart(request.session.get("user_email"))
    cart_item=CartItem.objects.filter(cart=cart,product_id=product_id).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1 
            cart_item.save()
            messages.success(request, f"Updated quantity of {cart_item.product.name} to {cart_item.quantity}.")

        else:
            cart_item.delete()
            messages.success(request, f" {cart_item.product.name} was removed from the cart.")

    else:
        messages.error(request,"Item not found in your cart.")

    return redirect("cart_view")

def Cart_Totle_Count(request):
    if not request.session.get('user_id'):
        return JsonResponse({"error": "Please log in to update your cart."}, status=403)

    cart = get_or_create_cart(request.session['user_email'])
    cart_items = cart.items.all()
    total_price = sum(item.product.discount * item.quantity for item in cart_items)
    

    return JsonResponse({"total_price": total_price}, status=200)



def clear_cart(request):
    # Check if the user is logged in
    if not request.session.get('user_id'):
        messages.error(request, "Please log in to clear your cart.")
        return redirect('login')

    # Get the user's cart
    cart = get_or_create_cart(request.session.get('user_email'))

    if cart:
        # Clear all items in the cart
        CartItem.objects.filter(cart=cart).delete()
        messages.success(request, "Your cart has been cleared.")
    else:
        messages.error(request, "Cart not found.")

    # Redirect to the cart view
    return redirect('home')
