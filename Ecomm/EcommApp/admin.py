from django.contrib import admin
from .models.user import User
from .models.category import Category
from .models.product import Product
from .models.wishlist import Wishlist
from .models.checkout import Chckout,Order,OrderItem,Payment,ShippingAddress
from .models.blog import BlogPost

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Chckout)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(ShippingAddress)
admin.site.register(BlogPost)
