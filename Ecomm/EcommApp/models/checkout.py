from django.db import models
from .user import User
from .product import Product

class ShippingAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="shipping_address")
    fname=models.CharField(max_length=40)
    lname=models.CharField(max_length=40)
    email=models.CharField(max_length=100)
    address1=models.CharField(max_length=255)
    address2=models.CharField(max_length=255,blank=True,null=True)
    city=models.CharField(max_length=40)
    state=models.CharField(max_length=40)
    # country=charF(blank_label='(select country)')
    zip_code=models.IntegerField(default=0)


    def __str__(self):
        return f"{self.fname} {self.lname} - {self.city}"

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")
    shipping_address=models.ForeignKey(ShippingAddress,on_delete=models.SET_NULL,null=True)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=50,choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ],default='pending')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.fname}"

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"
    
class Payment(models.Model):
    order=models.OneToOneField(Order,on_delete=models.CASCADE,related_name="payment")
    payment_method=models.CharField(max_length=50,choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cod', 'Cash on Delivery')
    ])
    payment_status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ], default='pending')
    transaction_id=models.CharField(max_length=255,blank=True,null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def __str__(self):
        return f"Payment for Order #{self.order.id}"


class Chckout(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="checkouts")
    fname = models.CharField(max_length=40)
    lname = models.CharField(max_length=40)
    # phone = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    # country = models.CharField(max_length=40)
    zip_code = models.CharField(max_length=20)
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    payment_method = models.CharField(max_length=50, choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cod', 'Cash on Delivery')
    ])
    payment_status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ], default='pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Order Items (as a JSON field to handle multiple items dynamically)
    items = models.JSONField(default=list)  # List of dictionaries to store product details
    
    def __str__(self):
        return f"Checkout - {self.user.username} - {self.total_amount}"