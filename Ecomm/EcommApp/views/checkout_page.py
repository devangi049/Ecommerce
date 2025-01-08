from django.shortcuts import render,redirect
from EcommApp.models.checkout import ShippingAddress,Order,OrderItem,Payment
from EcommApp.models.product import Product
from django.contrib import messages
from EcommApp.views.cart_utils import get_or_create_cart
from EcommApp.models.user import User
from EcommApp.models.cart import CartItem,Cart


def Chckout_Page(request):
    if not request.session['user_id']:
        messages.error(request, "Please log in to view your cart.")
        return redirect('login')

    cart = get_or_create_cart(request.session['user_email'])
    cart_items = cart.items.all()

    # Calculate total price
    total_price = sum(item.product.discount * item.quantity for item in cart_items)

    # Pass total_price to the template
    return render(request, "checkoutPage.html", {"cart_items": cart_items, "total_price": total_price})

def Checkout_View(request):
    if request.method == 'POST':
        shipping_address = None  # Initialize shipping_address with a default value
        try:
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            # country = request.POST.get('country')
            zip_code = request.POST.get('zip_code')
            payment_method = request.POST.get('payment_method')

            u_id = int(request.session['user_id'])
            user = User.objects.get(id=u_id)
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart)

            total_amount = sum(item.product.discount * item.quantity for item in cart_items)

            # Create the shipping address
            shipping_address = ShippingAddress.objects.create(
                user=user,
                fname=fname,
                lname=lname,
                email=email,
                address1=address1,
                address2=address2,
                city=city,
                state=state,
                # country=country,
                zip_code=zip_code,
            )
            shipping_address.save()

            print("shipping_address:", shipping_address)

            # Create the order
            order = Order.objects.create(
                user=user,
                shipping_address=shipping_address,
                total_amount=total_amount,
                status='pending'
            )
            order.save()

            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.discount
                )

            # Create the payment
            payment = Payment.objects.create(
                order=order,
                payment_method=payment_method,
                payment_status='pending',
                amount_paid=total_amount
            )
            payment.save()

            # Clear the cart
            cart.items.all().delete()

            messages.success(request, "Order placed successfully!")
            print("Order placed")
            return redirect("home")
        except Exception as e:
            print(f"Error in order creation. Shipping address: {shipping_address}")
            print(f"Error: {str(e)}")
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('cart_view')
    return render(request, 'checkoutPage.html')
